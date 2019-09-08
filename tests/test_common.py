# coding: utf-8
from __future__ import unicode_literals

import pytest
from spacy.tokens import Doc, Token


def test_common_installs(NLP):
    pass


def test_common_doc_tokens(NLP):
    doc = NLP("Lorem ipsum dolor sit amet.")
    assert len(doc) > 1
    assert isinstance(doc, Doc)
    assert all(isinstance(token, Token) for token in doc)


def test_common_vocab_lex_attrs(NLP):
    doc = Doc(NLP.vocab, words=["Lorem", "IPSUM", "dolor", "."])
    assert doc[0].is_title
    assert doc[1].is_upper
    assert doc[2].is_lower
    assert doc[3].is_punct


@pytest.mark.requires("parser")
def test_common_parser(NLP):
    """Ensure that parser exists and Doc.is_parsed."""
    assert "parser" in NLP.pipe_names
    doc = NLP("Lorem ipsum dolor sit amet.")
    assert doc.is_parsed


@pytest.mark.parametrize("text", ["Lorem ipsum."])
def test_common_parser_no_empty(NLP, text):
    """Ensure that labels aren't empty."""
    doc = NLP(text)
    assert all(t.dep != 0 for t in doc)
    assert all(t.dep_ for t in doc)
    assert any(t.dep != i for i, t in enumerate(doc))


@pytest.mark.requires("tagger")
def test_common_tagger(NLP):
    """Ensure that tagger exists and Doc.is_tagged."""
    assert "tagger" in NLP.pipe_names
    doc = NLP("Lorem ipsum dolor sit amet.")
    assert doc.is_tagged


@pytest.mark.requires("tagger")
@pytest.mark.parametrize(
    "text", ["Lorem ipsum.", pytest.param("Lorem — ipsum.", marks=pytest.mark.xfail())]
)
def test_common_tagger_no_empty(NLP, text):
    """Ensure that tags aren't empty."""
    doc = NLP(text)
    assert all(t.pos != 0 for t in doc)
    assert all(t.pos_ for t in doc)
    assert all(t.tag != 0 for t in doc)
    assert all(t.tag_ for t in doc)


@pytest.mark.requires("ner")
def test_common_ner(NLP):
    assert "ner" in NLP.pipe_names


def test_common_issue1242_issue1380(NLP):
    doc = NLP("")
    assert len(doc) == 0
    docs = list(NLP.pipe(["", "hello"]))
    assert len(docs[0]) == 0
    assert len(docs[1]) == 1


@pytest.mark.xfail(reason="Currently fails on Spanish. Investigate!")
@pytest.mark.requires("tagger", "parser")
def test_common_issue1253(NLP):
    def iter_doc(doc):
        for i in range(len(doc) - 1):
            for j in range(i + 1, len(doc)):
                doc[i:j].root

    tagger = NLP.get_pipe("tagger")
    parser = NLP.get_pipe("parser")
    doc = NLP.tokenizer("Highly rated - I'll definitely")
    tagger(doc)
    parser(doc)
    parser(doc)
    iter_doc(doc)


def test_common_issue1919(nlp):
    opt = nlp.begin_training()
