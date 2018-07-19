# coding: utf-8
from __future__ import unicode_literals

import pytest
import spacy
from pathlib import Path


OPT_MODEL = '--model'
OPT_LANG = '--lang'
OPT_VECTORS = '--has-vectors'
OPT_PARSER = '--has-parser'
OPT_TAGGER = '--has-tagger'
OPT_NER = '--has-ner'

OPT_MAPPING = {
    'tagger': OPT_TAGGER,
    'parser': OPT_PARSER,
    'ner': OPT_NER,
    'vectors': OPT_VECTORS
}


def pytest_addoption(parser):
    parser.addoption(OPT_MODEL, action='store', help='Model to test', required=True)
    parser.addoption(OPT_LANG, action='store', help='Model language', required=True)
    parser.addoption(OPT_VECTORS, action='store_true', help='Model has vectors')
    parser.addoption(OPT_PARSER, action='store_true', help='Model has parser')
    parser.addoption(OPT_TAGGER, action='store_true', help='Model has tagger')
    parser.addoption(OPT_NER, action='store_true', help='Model has NER')


def pytest_ignore_collect(path, config):
    lang = config.getoption(OPT_LANG)
    rel_path = Path(path).relative_to(Path(__file__).parent)
    tree = rel_path.parts
    if len(tree) > 2 and tree[0] == 'lang':
        if tree[1] != lang and tree[2].startswith('test_'):
            print('Ignoring', rel_path, '(language)')
            return True
        test_type = rel_path.stem.split('test_')[-1]
        test_type_opt = OPT_MAPPING.get(test_type)
        if test_type and test_type_opt and not config.getoption(test_type_opt):
            print("Ignoring", rel_path, '(model feature)')
            return True


def pytest_collection_modifyitems(config, items):
    for item in items:
        features = item.get_marker('requires')
        feature_args = features.args if features else []
        for arg in feature_args:
            expect = OPT_MAPPING.get(arg)
            if expect and not item.config.getoption(expect):
                reason = 'requires {} but --{} not set'.format(arg, expect)
                item.add_marker(pytest.mark.skip(reason=reason))


def pytest_report_header(config):
    return ["Model: {}".format(config.getoption(OPT_MODEL)),
            "Language: {}".format(config.getoption(OPT_LANG))]


@pytest.fixture(scope='session')
def NLP(request):
    name = request.config.getoption(OPT_MODEL)
    return spacy.load(name)

@pytest.fixture
def nlp(request):
    name = request.config.getoption(OPT_MODEL)
    return spacy.load(name)
