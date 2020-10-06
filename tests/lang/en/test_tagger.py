import pytest
from spacy.symbols import SPACE
from spacy.tokens import MorphAnalysis
from pathlib import Path
from ...util import json_path_to_examples


TEST_FILES_DIR = Path(__file__).parent / "test_files"


def test_en_tagger_tag_names(NLP):
    doc = NLP("I ate pizzas with anchovies.", disable=["parser"])
    assert type(doc[2].pos) == int
    assert isinstance(doc[2].pos_, str)
    assert isinstance(doc[2].dep_, str)
    assert doc[2].tag_ == "NNS"


@pytest.mark.xfail()
def test_en_tagger_example(NLP):
    doc = NLP("Apple is looking at buying U.K. startup")
    pos = ["PROPN", "AUX", "VERB", "ADP", "VERB", "PROPN", "NOUN"]
    tags = ["NNP", "VBZ", "VBG", "IN", "VBG", "NNP", "NN"]
    for token, expected_pos in zip(doc, pos):
        assert token.pos_ == expected_pos
    for token, expected_tag in zip(doc, tags):
        assert token.tag_ == expected_tag


@pytest.mark.parametrize(
    "test_file,accuracy_threshold",
    [("en_pud-ud-test.json", 0.94), ("masc-penn-treebank-sample.json", 0.88)],
)
def test_en_tagger_corpus(NLP, test_file, accuracy_threshold):
    data_path = TEST_FILES_DIR / test_file
    if not data_path.exists():
        raise FileNotFoundError("Test corpus not found", data_path)
    examples = json_path_to_examples(data_path, NLP)
    scores = NLP.evaluate(examples)

    assert scores["tag_acc"] > accuracy_threshold


def test_en_tagger_spaces(NLP):
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


def test_en_tagger_return_char(NLP):
    """Ensure spaces are assigned the POS tag SPACE"""
    text = (
        "hi Aaron,\r\n\r\nHow is your schedule today, I was wondering if "
        "you had time for a phone\r\ncall this afternoon?\r\n\r\n\r\n"
    )
    doc = NLP(text)
    for token in doc:
        if token.is_space:
            print(token.pos_)
            assert token.pos == SPACE
    assert doc[3].text == "\r\n\r\n"
    assert doc[3].is_space
    assert doc[3].pos == SPACE


def test_en_tagger_lemma_doc(NLP):
    doc = NLP("bleed")
    assert doc[0].lemma_ == "bleed"


@pytest.mark.parametrize(
    "text,lemmas,morphology",
    [
        ("aardwolves", ["aardwolf"], "Number=Plur"),
        ("aardwolf", ["aardwolf"], "Number=Sing"),
        ("planets", ["planet"], "Number=Plur"),
        ("ring", ["ring"], "Number=Sing"),
        pytest.param("axes", ["axe", "ax", "axis"], "Number=Plur", marks=pytest.mark.xfail()),
    ],
)
def test_en_tagger_lemma_nouns(NLP, text, lemmas, morphology):
    # Cases like this are problematic - not clear what we should do to resolve
    # ambiguity? ("axes", ["ax", "axes", "axis"])
    # noun_index = lemmatizer.index["noun"]
    # noun_exc = lemmatizer.exc["noun"]
    doc = NLP.make_doc(text)
    doc[0].morph = MorphAnalysis(NLP.vocab, morphology)
    doc[0].pos_ = "NOUN"
    NLP.get_pipe("lemmatizer")(doc)
    assert doc[0].lemma_ == lemmas[0]


@pytest.mark.parametrize(
    "text,lemmas",
    [("bleed", ["bleed"]), ("feed", ["feed"]), ("need", ["need"]), ("ring", ["ring"])],
)
def test_en_tagger_lemma_verbs(NLP, text, lemmas):
    doc = NLP.make_doc(text)
    doc[0].morph = MorphAnalysis(NLP.vocab, "VerbForm=Inf")
    doc[0].pos_ = "VERB"
    NLP.get_pipe("lemmatizer")(doc)
    assert doc[0].lemma_ == lemmas[0]


def test_en_tagger_lemma_base_forms(NLP):
    doc = NLP.make_doc("dive")
    doc[0].morph = MorphAnalysis(NLP.vocab, "Number=Sing")
    doc[0].pos_ = "NOUN"
    NLP.get_pipe("lemmatizer")(doc)
    assert doc[0].lemma_ == "dive"
    doc = NLP.make_doc("diva")
    doc[0].morph = MorphAnalysis(NLP.vocab, "Number=Plur")
    doc[0].pos_ = "NOUN"
    NLP.get_pipe("lemmatizer")(doc)
    assert doc[0].lemma_ == "diva"


def test_en_tagger_lemma_base_form_verb(NLP):
    doc = NLP.make_doc("saw")
    doc[0].morph = MorphAnalysis(NLP.vocab, "VerbForm=Past")
    doc[0].pos_ = "VERB"
    NLP.get_pipe("lemmatizer")(doc)
    assert doc[0].lemma_ == "see"


def test_en_tagger_lemma_punct(NLP):
    doc = NLP.make_doc("“ ” ‘ ’")
    for token in doc:
        token.pos_ = "PUNCT"
    NLP.get_pipe("lemmatizer")(doc)
    assert doc[0].lemma_ == '"'
    assert doc[1].lemma_ == '"'
    assert doc[2].lemma_ == "'"
    assert doc[3].lemma_ == "'"


def test_en_tagger_lemma_assignment(NLP):
    doc = NLP("Bananas in pyjamas are geese.")
    assert all(t.lemma_ != "" for t in doc)


def test_en_tagger_lemma_issue1305(NLP):
    """Test lemmatization of English VBZ."""
    doc = NLP("This app works well")
    print([t.pos_ for t in doc])
    print([t.lemma_ for t in doc])
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
        ("colocalizes", ["colocalize"]),
    ],
)
def test_en_tagger_lemma_issue781(NLP, word, lemmas):
    doc = NLP.make_doc(word)
    doc[0].pos_ = "NOUN"
    doc[0].morph = MorphAnalysis(NLP.vocab, "Number=Plur")
    NLP.get_pipe("lemmatizer")(doc)
    assert doc[0].lemma_ == lemmas[0]


@pytest.mark.skip(reason="No more -PRON- lemmas")
@pytest.mark.parametrize("text", ["He is the man", "he is the man"])
def test_en_tagger_lemma_issue686(NLP, text):
    """Test that pronoun lemmas are assigned correctly."""
    tokens = NLP(text)
    assert tokens[0].lemma_ == "-PRON-"
