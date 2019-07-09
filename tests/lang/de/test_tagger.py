# coding: utf-8
from __future__ import unicode_literals

import os
import pytest
from spacy.tokens import Doc
from spacy.compat import unicode_
from spacy.parts_of_speech import SPACE
from spacy.gold import GoldCorpus
from spacy import util

# from spacy.lemmatizer import lemmatize

TEST_FILES_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_files',
)


@pytest.fixture
def lemmatizer(NLP):
    return NLP.Defaults.create_lemmatizer()


def test_de_tagger_tag_names(NLP):
    doc = NLP("Ich esse eine Pizza mit Tomaten.", disable=["parser"])
    assert type(doc[3].pos) == int
    assert isinstance(doc[3].pos_, unicode_)
    assert isinstance(doc[3].dep_, unicode_)
    assert doc[3].tag_ == "NN"


def test_de_tagger_example(NLP):
    doc = NLP("Zwischen 1950 und 1955 führte er eine Reform ein.")
    tags = ["APPR", "CARD", "KON", "CARD", "VVFIN", "PPER", "ART", "NN", "PTKVZ", "$."]
    for token, expected_tag in zip(doc, tags):
        assert token.tag_ == expected_tag


# This threshold is artificially low due to problems with spacy 2.1. (#3830)
@pytest.mark.parametrize(
    "test_file,accuracy_threshold",
    [("de_pud-ud-test.stts.json", 93)]
)
def test_de_tagger_corpus(NLP, test_file, accuracy_threshold):
    data_path = os.path.join(TEST_FILES_DIR, test_file)
    data_path = util.ensure_path(data_path)
    if not data_path.exists():
        raise FileNotFoundError("Test corpus not found", data_path)
    corpus = GoldCorpus(data_path, data_path)
    dev_docs = list(corpus.dev_docs(NLP, gold_preproc=False))
    scorer = NLP.evaluate(dev_docs)

    assert scorer.tags_acc > accuracy_threshold


@pytest.mark.parametrize(
    "test_file",
    ["de_pud-ud-test.stts.json"]
)
def test_de_tagger_tagset(NLP, test_file):
    """Check that no tags outside the tagset are used."""
    gold_tags = {"$(", "$,", "$.", "ADJA", "ADJD", "ADV", "APPO", "APPR", "APPRART", "APZR", "ART", "CARD", "FM", "ITJ",
                 "KOKOM", "KON", "KOUI", "KOUS", "NE", "NN", "NNE", "PDAT", "PDS", "PIAT", "PIS", "PPER", "PPOSAT",
                 "PPOSS", "PRELAT", "PRELS", "PRF", "PROAV", "PTKA", "PTKANT", "PTKNEG", "PTKVZ", "PTKZU", "PWAT",
                 "PWAV", "PWS", "TRUNC", "VAFIN", "VAIMP", "VAINF", "VAPP", "VMFIN", "VMINF", "VMPP", "VVFIN", "VVIMP",
                 "VVINF", "VVIZU", "VVPP", "XY"}

    data_path = os.path.join(TEST_FILES_DIR, test_file)
    data_path = util.ensure_path(data_path)
    if not data_path.exists():
        raise FileNotFoundError("Test corpus not found", data_path)
    corpus = GoldCorpus(data_path, data_path)
    dev_docs = list(corpus.dev_docs(NLP, gold_preproc=False))

    pred_tags = set()
    tagger = NLP.get_pipe('tagger')

    for doc, _ in dev_docs:
        tagger(doc)
        pred_tags = pred_tags.union(set([t.tag_ for t in doc]))

    assert len(pred_tags - gold_tags) == 0


@pytest.mark.xfail
def test_de_tagger_spaces(NLP):
    """Ensure spaces are assigned the POS tag SPACE"""
    doc = NLP("Manche\nLeerzeichen sind\terforderlich.")
    assert doc[0].pos != SPACE
    assert doc[0].pos_ != "SPACE"
    assert doc[1].pos == SPACE
    assert doc[1].pos_ == "SPACE"
    assert doc[1].tag_ == "SP"
    assert doc[2].pos != SPACE
    assert doc[3].pos != SPACE
    assert doc[4].pos == SPACE


def test_de_tagger_return_char(NLP):
    """Ensure spaces are assigned the POS tag SPACE"""
    text = (
        "Hallo Aaron,\r\n\r\nwie geht's Dir? "
        "Können wir heute\r\nNachmittag telefonieren?\r\n\r\n\r\n"
    )
    doc = NLP(text)
    for token in doc:
        if token.is_space:
            assert token.pos == SPACE
    assert doc[3].text == "\r\n\r\n"
    assert doc[3].is_space
    assert doc[3].pos == SPACE


@pytest.mark.xfail
@pytest.mark.parametrize(
    "text,pos,tags",
    [
        ('"Altbau-Wohnung".',
         ["PUNCT", "NOUN", "PUNCT", "PUNCT"],
         ["$(", "NN", "$(", "$."]),
        ("„Altbau-Wohnung“ — „Neubau-Wohnung“",
         ["PUNCT", "NOUN", "PUNCT", "PUNCT", "PUNCT", "NOUN", "PUNCT"],
         ["$(", "NN", "$(", "$(", "$(", "NN", "$("]),
        ("Du und ich –",
         ["PRON", "CONJ", "PRON", "PUNCT"],
         ["PPER", "KON", "PPER", "$("]),
        ("Farben: rot, blau! (Auch lila?)",
         ["NOUN", "PUNCT", "ADJ", "PUNCT", "ADJ", "PUNCT", "PUNCT", "ADV", "ADJ", "PUNCT", "PUNCT"],
         ["NN", "$.", "ADJD", "$,", "ADJD", "$.", "$(", "ADV", "ADJD", "$.", "$("]),
    ],
)
def test_de_tagger_punctuation(NLP, text, pos, tags):
    """Ensure punctuation is tagged correctly"""
    doc = NLP(text)
    for token, expected_pos in zip(doc, pos):
        assert token.pos_ == expected_pos
    for token, expected_tag in zip(doc, tags):
        assert token.tag_ == expected_tag


def test_de_tagger_lemma_doc(NLP, lemmatizer):
    doc = Doc(NLP.vocab, words=["gegessen"])
    doc[0].tag_ = "VVPP"
    assert doc[0].lemma_ == "essen"


def test_de_tagger_lemma_assignment(NLP):
    doc = NLP("Bananen in Schlafanzügen sind Gänse.")
    assert all(t.lemma_ != "" for t in doc)


@pytest.mark.xfail
def test_de_tagger_lemma_punct(lemmatizer):
    assert lemmatizer.punct("“") == ['"']
    assert lemmatizer.punct("”") == ['"']


# The following tests do not test the behavior of the current German
# lemmatizer, which has a lot of weird and inconsistent cases.
#
# Weird (but consistent except for individual corrections like for "Rang" in
# #2537):
#
#    Form -> formen, Schimmel -> schimmeln (as imperatives instead of nouns)
#
# Both inconsistent and weird:
#
#    mir -> sich / Mir -> ich
# 
# While a token-based lookup lemmatizer is never going to work that well for
# German, it looks like a lot of weirdness and inconsistencies were introduced
# in https://github.com/michmech/lemmatization-lists/ . (The original resources
# look more consistent and also include POS information.)
@pytest.mark.xfail
def test_de_tagger_lemma_base_forms(lemmatizer):
    assert lemmatizer.noun("Schimmel") == ["Schimmel"]
    assert lemmatizer.noun("Schimmeln") == ["Schimmel"]


@pytest.mark.xfail
@pytest.mark.parametrize("text", ["Er ist wieder da", "er ist wieder da"])
def test_de_tagger_lemma_issue686(NLP, text):
    """Test that pronoun lemmas are assigned correctly."""
    tokens = NLP(text)
    assert tokens[0].lemma_ == "er"


@pytest.mark.xfail
@pytest.mark.parametrize(
    "text1,text2",
    [
        ("Dort gibt's einen Bäcker", "Dort gibt es einen Bäcker"),
    ],
)
def test_de_tagger_lemma_issue717(NLP, text1, text2):
    """Test that contractions are assigned the correct lemma."""
    doc1 = NLP(text1)
    doc2 = NLP(text2)
    assert doc1[2].lemma_ == doc2[2].lemma_
    assert doc1[2].lemma == doc2[2].lemma
