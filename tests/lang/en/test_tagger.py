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


def test_en_tagger_tag_names(NLP):
    doc = NLP("I ate pizzas with anchovies.", disable=["parser"])
    assert type(doc[2].pos) == int
    assert isinstance(doc[2].pos_, unicode_)
    assert isinstance(doc[2].dep_, unicode_)
    assert doc[2].tag_ == "NNS"


def test_en_tagger_example(NLP):
    doc = NLP("Apple is looking at buying U.K. startup")
    pos = ["PROPN", "VERB", "VERB", "ADP", "VERB", "PROPN", "NOUN"]
    tags = ["NNP", "VBZ", "VBG", "IN", "VBG", "NNP", "NN"]
    for token, expected_pos in zip(doc, pos):
        assert token.pos_ == expected_pos
    for token, expected_tag in zip(doc, tags):
        assert token.tag_ == expected_tag

@pytest.mark.parametrize(
    "test_file,accuracy_threshold",
    [
        ("en_pud-ud-test.json", 94), 
        ("masc-penn-treebank-sample.json", 87)
    ],
)
def test_en_tagger_corpus(NLP, test_file, accuracy_threshold):
    data_path = os.path.join(TEST_FILES_DIR, test_file)
    data_path = util.ensure_path(data_path)
    if not data_path.exists():
        raise FileNotFoundError("Test corpus not found", data_path)
    corpus = GoldCorpus(data_path, data_path)
    dev_docs = list(corpus.dev_docs(NLP, gold_preproc=False))
    scorer = NLP.evaluate(dev_docs)

    assert scorer.tags_acc > accuracy_threshold

@pytest.mark.xfail
def test_en_tagger_spaces(NLP):
    """Ensure spaces are assigned the POS tag SPACE"""
    doc = NLP("Some\nspaces are\tnecessary.")
    assert doc[0].pos != SPACE
    assert doc[0].pos_ != "SPACE"
    assert doc[1].pos == SPACE
    assert doc[1].pos_ == "SPACE"
    assert doc[1].tag_ == "SP"
    assert doc[2].pos != SPACE
    assert doc[3].pos != SPACE
    assert doc[4].pos == SPACE


def test_en_tagger_return_char(NLP):
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


def test_en_tagger_lemma_doc(NLP, lemmatizer):
    doc = Doc(NLP.vocab, words=["bleed"])
    doc[0].tag_ = "VBP"
    assert doc[0].lemma_ == "bleed"


@pytest.mark.parametrize(
    "text,lemmas,morphology",
    [
        ("aardwolves", ["aardwolf"], {"Number": "plur"}),
        ("aardwolf", ["aardwolf"], {"Number": "sing"}),
        ("planets", ["planet"], {"Number": "plur"}),
        ("ring", ["ring"], {"Number": "sing"}),
        ("axes", ["axe", "ax", "axis"], {"Number": "plur"}),
    ],
)
def test_en_tagger_lemma_nouns(lemmatizer, text, lemmas, morphology):
    # Cases like this are problematic - not clear what we should do to resolve
    # ambiguity? ("axes", ["ax", "axes", "axis"])
    # noun_index = lemmatizer.index["noun"]
    # noun_exc = lemmatizer.exc["noun"]
    # noun_rules = lemmatizer.rules["noun"]
    lemmas.sort()
    assert sorted(lemmatizer.noun(text, morphology=morphology)) == lemmas


@pytest.mark.parametrize(
    "text,lemmas",
    [("bleed", ["bleed"]), ("feed", ["feed"]), ("need", ["need"]), ("ring", ["ring"])],
)
def test_en_tagger_lemma_verbs(lemmatizer, text, lemmas):
    assert lemmatizer.noun(text) == lemmas


def test_en_tagger_lemma_base_forms(lemmatizer):
    assert lemmatizer.noun("dive", {"Number": "sing"}) == ["dive"]
    assert lemmatizer.noun("dive", {"Number": "plur"}) == ["diva"]


def test_en_tagger_lemma_base_form_verb(lemmatizer):
    assert lemmatizer.verb("saw", {"verbform": "past"}) == ["see"]


def test_en_tagger_lemma_punct(lemmatizer):
    assert lemmatizer.punct("“") == ['"']
    assert lemmatizer.punct("”") == ['"']
    assert lemmatizer.punct("‘") == ["'"]
    assert lemmatizer.punct("’") == ["'"]


def test_en_tagger_lemma_assignment(NLP):
    doc = NLP("Bananas in pyjamas are geese.")
    assert all(t.lemma_ != "" for t in doc)


def test_en_tagger_lemma_issue1305(NLP):
    """Test lemmatization of English VBZ."""
    assert NLP.vocab.morphology.lemmatizer("works", "verb") == ["work"]
    doc = NLP("This app works well")
    assert doc[2].lemma_ == "work"


@pytest.mark.parametrize(
    "text,i", [("Jane's got a new car", 1), ("Jane thinks that's a nice car", 3)]
)
def test_en_tagger_lemma_issue401_issue719(NLP, text, i):
    """Text that 's in contractions is not lemmatized as ' or empty string."""
    doc = NLP(text)
    assert doc[i].lemma_ != "'"
    assert doc[i].lemma_ != ""


@pytest.mark.parametrize(
    "text1,text2",
    [
        ("You're happy", "You are happy"),
        ("I'm happy", "I am happy"),
        ("he's happy", "he's happy"),
    ],
)
def test_en_tagger_lemma_issue717(NLP, text1, text2):
    """Test that contractions are assigned the correct lemma."""
    doc1 = NLP(text1)
    doc2 = NLP(text2)
    assert doc1[1].lemma_ == doc2[1].lemma_
    assert doc1[1].lemma == doc2[1].lemma


@pytest.mark.parametrize(
    "word,lemmas",
    [
        ("chromosomes", ["chromosome"]),
        ("endosomes", ["endosome"]),
        ("colocalizes", ["colocaliz", "colocalize"]),
    ],
)
def test_en_tagger_lemma_issue781(lemmatizer, word, lemmas):
    result = lemmatizer(word, "noun", morphology={"Number": "plur"})
    assert sorted(result) == sorted(lemmas)


@pytest.mark.parametrize("text", ["He is the man", "he is the man"])
def test_en_tagger_lemma_issue686(NLP, text):
    """Test that pronoun lemmas are assigned correctly."""
    tokens = NLP(text)
    assert tokens[0].lemma_ == "-PRON-"
