import pytest
from spacy.tokens import Doc
from spacy.symbols import SPACE
from pathlib import Path
from ...util import evaluate_corpus, json_path_to_examples


TEST_FILES_DIR = Path(__file__).parent / "test_files"


def test_de_tagger_tag_names(NLP):
    doc = NLP("Ich esse eine Pizza mit Tomaten.", disable=["parser"])
    assert type(doc[3].pos) == int
    assert isinstance(doc[3].pos_, str)
    assert isinstance(doc[3].dep_, str)
    assert doc[3].tag_ == "NN"


def test_de_tagger_example(NLP):
    doc = NLP("Zwischen 1950 und 1955 führte er eine Reform ein.")
    tags = ["APPR", "CARD", "KON", "CARD", "VVFIN", "PPER", "ART", "NN", "PTKVZ", "$."]
    for token, expected_tag in zip(doc, tags):
        assert token.tag_ == expected_tag


# This threshold is artificially low due to problems with spacy 2.1. (#3830)
@pytest.mark.parametrize(
    "test_file,accuracy_threshold", [("de_pud-ud-test.stts.json", 0.93)]
)
def test_de_tagger_corpus(NLP, test_file, accuracy_threshold):
    data_path = TEST_FILES_DIR / test_file
    evaluate_corpus(data_path, NLP, {"tag_acc": accuracy_threshold})


@pytest.mark.parametrize("test_file", ["de_pud-ud-test.stts.json"])
def test_de_tagger_tagset(NLP, test_file):
    """Check that no tags outside the tagset are used."""
    # fmt: off
    gold_tags = {"$(", "$,", "$.", "ADJA", "ADJD", "ADV", "APPO", "APPR",
                 "APPRART", "APZR", "ART", "CARD", "FM", "ITJ", "KOKOM", "KON",
                 "KOUI", "KOUS", "NE", "NN", "NNE", "PDAT", "PDS", "PIAT",
                 "PIS", "PPER", "PPOSAT", "PPOSS", "PRELAT", "PRELS", "PRF",
                 "PROAV", "PTKA", "PTKANT", "PTKNEG", "PTKVZ", "PTKZU", "PWAT",
                 "PWAV", "PWS", "TRUNC", "VAFIN", "VAIMP", "VAINF", "VAPP",
                 "VMFIN", "VMINF", "VMPP", "VVFIN", "VVIMP", "VVINF", "VVIZU",
                 "VVPP", "XY"}
    # fmt: on
    data_path = TEST_FILES_DIR / test_file
    if not data_path.exists():
        raise FileNotFoundError("Test corpus not found", data_path)
    examples = json_path_to_examples(data_path, NLP)
    tagger = NLP.get_pipe("tagger")
    pred_tags = set()
    for example in examples:
        doc = example.predicted
        tagger(doc)
        pred_tags = pred_tags.union(set([t.tag_ for t in doc]))
    assert len(pred_tags - gold_tags) == 0


def test_de_tagger_spaces(NLP):
    """Ensure spaces are assigned the POS tag SPACE"""
    doc = NLP("Manche\nLeerzeichen sind\terforderlich.")
    assert doc[0].pos != SPACE
    assert doc[0].pos_ != "SPACE"
    assert doc[1].pos == SPACE
    assert doc[1].pos_ == "SPACE"
    assert doc[1].tag_ == "_SP"
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


@pytest.mark.parametrize(
    "text,pos,tags",
    # fmt: off
    [
        ('"Altbau-Wohnung".',
         ["PUNCT", "NOUN", "PUNCT", "PUNCT"],
         ["$(", "NN", "$(", "$."]),
        ("„Altbau-Wohnung“ — „Neubau-Wohnung“",
         ["PUNCT", "NOUN", "PUNCT", "PUNCT", "PUNCT", "NOUN", "PUNCT"],
         ["$(", "NN", "$(", "$(", "$(", "NN", "$("]),
        ("Du und ich –",
         ["PRON", "CCONJ", "PRON", "PUNCT"],
         ["PPER", "KON", "PPER", "$("]),
        pytest.param("Farben: rot, blau! (Auch lila?)",
         ["NOUN", "PUNCT", "ADJ", "PUNCT", "ADJ", "PUNCT", "PUNCT", "ADV", "ADJ", "PUNCT", "PUNCT"],
         ["NN", "$.", "ADJD", "$,", "ADJD", "$.", "$(", "ADV", "ADJD", "$.", "$("], marks=pytest.mark.xfail()),
    ],
    # fmt: on
)
def test_de_tagger_punctuation(NLP, text, pos, tags):
    """Ensure punctuation is tagged correctly"""
    doc = NLP(text)
    doc_data = [(w.text, w.tag_, w.pos_) for w in doc]
    for token, expected_pos in zip(doc, pos):
        if token.is_punct:
            assert token.pos_ == expected_pos, doc_data
    for token, expected_tag in zip(doc, tags):
        if token.is_punct:
            assert token.tag_ == expected_tag, doc_data


@pytest.mark.xfail
def test_de_tagger_lemma_doc(NLP, lemmatizer):
    doc = Doc(NLP.vocab, words=["gegessen"])
    doc[0].tag_ = "VVPP"
    assert doc[0].lemma_ == "essen"


@pytest.mark.xfail
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
    "text1,text2", [("Dort gibt's einen Bäcker", "Dort gibt es einen Bäcker")]
)
def test_de_tagger_lemma_issue717(NLP, text1, text2):
    """Test that contractions are assigned the correct lemma."""
    doc1 = NLP(text1)
    doc2 = NLP(text2)
    assert doc1[2].lemma_ == doc2[2].lemma_
    assert doc1[2].lemma == doc2[2].lemma
