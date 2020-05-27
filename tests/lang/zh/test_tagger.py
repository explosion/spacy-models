# coding: utf-8
from __future__ import unicode_literals

import pytest
from spacy.tokens import Doc
from spacy.compat import unicode_
from spacy.parts_of_speech import SPACE
from spacy.gold import GoldCorpus
from pathlib import Path


TEST_FILES_DIR = Path(__file__).parent / "test_files"


@pytest.fixture
def lemmatizer(NLP):
    return NLP.vocab.morphology.lemmatizer


@pytest.mark.parametrize(
    "test_file,accuracy_threshold",
    [("zh_gsd-ud-dev_sample.json", 33)],
)
def test_zh_tagger_corpus(NLP, test_file, accuracy_threshold):
    data_path = TEST_FILES_DIR / test_file
    if not data_path.exists():
        raise FileNotFoundError("Test corpus not found", data_path)
    corpus = GoldCorpus(data_path, data_path)
    dev_docs = list(corpus.dev_docs(NLP, gold_preproc=False))
    scorer = NLP.evaluate(dev_docs)

    assert scorer.tags_acc > accuracy_threshold


def test_zh_tagger_spaces(NLP):
    """Ensure spaces are assigned the POS tag SPACE"""
    doc = NLP("作为语言而言，为世界使用人数最多的语言，  目前世界有五分之一人口做\n\n为母语。")
    for t in doc:
        if t.is_space:
            assert t.pos_ == "SPACE"
            assert t.tag_ == "_SP"
        else:
            assert t.pos_ != "SPACE"
            assert t.tag_ != "_SP"


def test_zh_tagger_return_char(NLP):
    """Ensure spaces are assigned the POS tag SPACE"""
    text = (
        "hi Aaron,\r\n\r\nHow is your schedule today, I was wondering if "
        "you had time for a phone\r\ncall this afternoon?\r\n\r\n\r\n"
    )
    doc = NLP(text)
    for t in doc:
        if t.is_space:
            assert t.pos_ == "SPACE"
