# coding: utf-8
from __future__ import unicode_literals

import collections
import csv
import os
from typing import Dict, List, Tuple

import pytest
import spacy
from pathlib import Path


spacy.prefer_gpu()


OPT_MODEL = "--model"
OPT_LANG = "--lang"
OPT_VECTORS = "--has-vectors"
OPT_PARSER = "--has-parser"
OPT_TAGGER = "--has-tagger"
OPT_MORPHOLOGIZER = "--has-morphologizer"
OPT_LEMMATIZER = "--has-lemmatizer"
OPT_NER = "--has-ner"
OPT_SEGMENTER = "--has-segmenter"

OPT_MAPPING = {
    "tagger": OPT_TAGGER,
    "morphologizer": OPT_MORPHOLOGIZER,
    "lemmatizer": OPT_LEMMATIZER,
    "parser": OPT_PARSER,
    "ner": OPT_NER,
    "vectors": OPT_VECTORS,
    "segmenter": OPT_SEGMENTER
}


def pytest_addoption(parser):
    parser.addoption(OPT_MODEL, action="store", help="Model to test", required=True)
    parser.addoption(OPT_LANG, action="store", help="Model language", required=True)
    parser.addoption(OPT_VECTORS, action="store_true", help="Model has vectors")
    parser.addoption(OPT_PARSER, action="store_true", help="Model has parser")
    parser.addoption(OPT_TAGGER, action="store_true", help="Model has tagger")
    parser.addoption(
        OPT_MORPHOLOGIZER, action="store_true", help="Model has morphologizer"
    )
    parser.addoption(OPT_LEMMATIZER, action="store_true", help="Model has lemmatizer")
    parser.addoption(OPT_NER, action="store_true", help="Model has NER")
    parser.addoption(OPT_SEGMENTER, action="store_true", help="Model has segmenter")


def pytest_ignore_collect(path, config):
    lang = config.getoption(OPT_LANG)
    rel_path = Path(path).relative_to(Path(__file__).parent)
    tree = rel_path.parts
    if len(tree) > 2 and tree[0] == "lang":
        if tree[1] != lang and tree[2].startswith("test_"):
            print("Ignoring", rel_path, "(language)")
            return True
        test_type = rel_path.stem.split("test_")[-1]
        test_type_opt = OPT_MAPPING.get(test_type)
        if test_type and test_type_opt and not config.getoption(test_type_opt):
            print("Ignoring", rel_path, "(model feature)")
            return True


def pytest_collection_modifyitems(config, items):
    for item in items:
        for requires in item.iter_markers("requires"):
            arg = requires.args[0]
            expect = OPT_MAPPING.get(arg)
            if expect and not item.config.getoption(expect):
                reason = "requires {} but --{} not set".format(arg, expect)
                item.add_marker(pytest.mark.skip(reason=reason))


def pytest_report_header(config):
    return [
        "Model: {}".format(config.getoption(OPT_MODEL)),
        "Language: {}".format(config.getoption(OPT_LANG)),
    ]


@pytest.fixture(scope="session")
def NLP(request):
    name = request.config.getoption(OPT_MODEL)
    return spacy.load(name)


@pytest.fixture
def nlp(request):
    name = request.config.getoption(OPT_MODEL)
    return spacy.load(name)


@pytest.fixture(scope="session")
def lang(request):
    return request.config.getoption(OPT_LANG)


def pytest_generate_tests(metafunc):
    """
    Initializes data generation hooks for tests. Useful e.g. for supplying tests with dynamically generated data
    depending on pytest configuration options.
    """

    # Extracts configurations for calls of evaluate_corpus(). This is done by parsing performance_thresholds.csv and
    # bundling all metrics with their respective thresholds per data file. This corresponds to the parameter sets for
    # individual calls of evaluate_corpus().
    if "corpus_evaluation_config" in metafunc.fixturenames:
        model_size = metafunc.config.getoption("model").split("_")[-1]
        lang = metafunc.config.getoption("lang")
        parameter_sets: Dict[str, List[Tuple[str, float]]] = {}

        with open(Path(__file__).parent / "data" / "performance_thresholds.csv") as threshold_file:
            for row in csv.DictReader(threshold_file):
                configs = parameter_sets.get(row["filename"], [])
                if metafunc.config.getoption(OPT_MAPPING[row["component"]]) and row["language"] == lang and (
                    # Ignore configs for other model sizes.
                    model_size == row["model_size"]
                    or
                    # If model_size is *, but specific model_size already set: skip config for generic model size.
                    row["model_size"] == "*"
                    and not any(
                        [c for c in configs if c[0] == row["metric"] and c[1] != "*"]
                    )
                ):
                    # If model_size is specific and generic model_size already defined: drop config for generic model
                    # size.
                    if row["model_size"] != "*" and any(
                        [c for c in configs if c[0] == row["metric"] and c[1] == "*"]
                    ):
                        configs = [
                            c for c in configs if c[0] != row["metric"] or c[1] != "*"
                        ]

                    parameter_sets[row["filename"]] = [
                        *configs,
                        (row["metric"], row["model_size"], float(row["accuracy"])),
                    ]

        # Ensure metric thresholds haven't been set ambiguously.
        duplicate_metrics = set()
        for key, count in collections.Counter(
            tuple(
                (filename, metric[0])
                for filename in parameter_sets
                for metric in parameter_sets[filename]
            )
        ).items():
            if count != 1:
                duplicate_metrics.add(key)
        assert (
            len(duplicate_metrics) == 0
        ), f"Metrics {duplicate_metrics} have been set more than once."

        # Ensure there is at least one config to execute.
        assert (
            len(parameter_sets) > 0
        ), "No parameter threshold configuration for this language and model size found."

        metafunc.parametrize(
            "corpus_evaluation_config",
            tuple(
                (filename, metric_thresholds)
                for filename, metric_thresholds in parameter_sets.items()
            ),
        )
