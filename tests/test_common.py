# coding: utf-8
from __future__ import unicode_literals

import pytest
import importlib
from spacy.tokens import Doc, Token


@pytest.fixture
def example_text(NLP):
    try:
        examples = importlib.import_module("spacy.lang." + NLP.lang + ".examples")
        sentences = examples.sentences
    except Exception:
        sentences = [
            "This is a sentence.",
            "This is another sentence.",
        ]
    # TODO: need a language-specific setting since space is not appropriate for
    # all languages
    punct_fixed = []
    sent_sep = " "
    for sent in sentences:
        if sent[-1].isalnum():
            if NLP.lang in ["ja", "zh"]:
                sent += "。"
                sent_sep = ""
            else:
                sent += "."
        punct_fixed.append(sent)
    return sent_sep.join(punct_fixed)


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
    assert doc.has_annotation("DEP", require_complete=True)


@pytest.mark.requires("parser")
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
    assert doc.has_annotation("TAG", require_complete=True)


@pytest.mark.requires("tagger")
@pytest.mark.parametrize(
    "text", ["Lorem ipsum.", pytest.param("Lorem — ipsum.", marks=pytest.mark.xfail())]
)
def test_common_tagger_no_empty(NLP, text):
    """Ensure that tags aren't empty."""
    doc = NLP(text)
    assert all(t.tag != 0 for t in doc)
    assert all(t.tag_ for t in doc)


@pytest.mark.requires("morphologizer")
def test_common_morphologizer(NLP):
    """Ensure that morphologizer exists and Doc.is_tagged."""
    assert "morphologizer" in NLP.pipe_names
    doc = NLP("Lorem ipsum dolor sit amet.")
    assert doc.has_annotation("MORPH", require_complete=True)


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


@pytest.mark.requires("tagger")
def test_tagger_sanity_checks(NLP, example_text):
    doc = NLP(example_text)
    # check that the labels are a subset of the meta model labels
    model_labels = set(NLP.meta["labels"]["tagger"])
    assert set([t.tag_ for t in doc]) <= model_labels
    # check that the labels are a subset of the pipe model labels
    model_labels = set(NLP.get_pipe("tagger").labels)
    assert set([t.tag_ for t in doc]) <= model_labels


@pytest.mark.requires("parser")
def test_parser_sanity_checks(NLP, example_text):
    doc = NLP(example_text)
    # check that sentences are split
    assert len(list(doc.sents)) > 1
    # check that the labels are a subset of the meta model labels
    model_labels = set(NLP.meta["labels"]["parser"])
    assert set([t.dep_ for t in doc]) <= model_labels | {""}
    # check that the labels are a subset of the pipe model labels
    model_labels = set(NLP.get_pipe("parser").labels)
    assert set([t.dep_ for t in doc]) <= model_labels | {""}


@pytest.mark.requires("ner")
def test_ner_sanity_checks(NLP, example_text):
    doc = NLP(example_text)
    # check that the labels are a subset of the meta model labels
    model_labels = set(NLP.meta["labels"]["ner"])
    assert set([t.ent_type_ for t in doc]) <= model_labels | {""}
    # check that the labels are a subset of the pipe model labels
    model_labels = set(NLP.get_pipe("ner").labels)
    assert set([t.ent_type_ for t in doc]) <= model_labels | {""}


@pytest.mark.skip(reason="Not the right check for v3")
def test_common_issue1919(nlp):
    nlp.begin_training()
