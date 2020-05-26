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
    [("fr_sequoia-ud-dev01_10.json", 91)],
)
def test_fr_tagger_corpus(NLP, test_file, accuracy_threshold):
    data_path = TEST_FILES_DIR / test_file
    if not data_path.exists():
        raise FileNotFoundError("Test corpus not found", data_path)
    corpus = GoldCorpus(data_path, data_path)
    dev_docs = list(corpus.dev_docs(NLP, gold_preproc=False))
    scorer = NLP.evaluate(dev_docs)

    assert scorer.tags_acc > accuracy_threshold


def test_fr_tagger_spaces(NLP):
    """Ensure spaces are assigned the POS tag SPACE"""
    doc = NLP("Some\nspaces are\tnecessary.")
    assert doc[0].pos != SPACE
    assert doc[0].pos_ != "SPACE"
    assert doc[1].pos == SPACE
    assert doc[1].pos_ == "SPACE"
    assert doc[1].tag_ == "_SP"
    assert doc[2].pos != SPACE
    assert doc[3].pos != SPACE
    assert doc[4].pos == SPACE


def test_fr_tagger_return_char(NLP):
    """Ensure spaces are assigned the POS tag SPACE"""
    text = (
        "hi Aaron,\r\n\r\nHow is your schedule today, I was wondering if "
        "you had time for a phone\r\ncall this afternoon?\r\n\r\n\r\n"
    )
    doc = NLP(text)
    for token in doc:
        if token.is_space:
            assert token.pos == SPACE
    assert doc[3].text == "\r\n\r\n"
    assert doc[3].is_space
    assert doc[3].pos == SPACE


@pytest.mark.xfail
def test_fr_tagger_issue2251(NLP):
    doc = NLP("Tu vas bien.")
    assert doc[0].tag_ == "PRON__Number=Sing|Person=2"
    doc = NLP("Comment vas-tu?")
    assert doc[3].tag_ == "PRON__Number=Sing|Person=2"
    assert doc[3].lemma_ == "tu"

@pytest.mark.xfail
def test_fr_tagger_issue1958(NLP):
    doc = NLP("Pour poser des congés, qu'est-ce que je fais ?")
    assert all(t.pos != 0 for t in doc)
    assert all(t.pos_ for t in doc)
    assert all(t.tag != 0 for t in doc)
    assert all(t.tag_ for t in doc)
