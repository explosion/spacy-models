# coding: utf-8
from __future__ import unicode_literals

import pytest
from spacy.gold import GoldCorpus
from pathlib import Path


TEST_FILES_DIR = Path(__file__).parent / "test_files"


@pytest.mark.xfail
@pytest.mark.parametrize("test_file", [("de_pud-ud-test.stts.json")])
def test_de_parser_depset(NLP, test_file):
    """Check that no tags outside the tagset are used."""
    gold_deps = set(NLP.get_pipe("parser").labels)
    data_path = TEST_FILES_DIR / test_file
    if not data_path.exists():
        raise FileNotFoundError("Test corpus not found", data_path)
    corpus = GoldCorpus(data_path, data_path)
    dev_docs = list(corpus.dev_docs(NLP, gold_preproc=False))
    pred_deps = set()
    parser = NLP.get_pipe("parser")
    for doc, _ in dev_docs:
        parser(doc)
        pred_deps = pred_deps.union(set([t.dep_ for t in doc]))
    assert len(pred_deps - gold_deps) == 0
