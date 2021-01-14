import pytest
from pathlib import Path
from spacy.symbols import SPACE
from ...util import evaluate_corpus


TEST_FILES_DIR = Path(__file__).parent / "test_files"


def test_ru_morphologizer_example(NLP):
    doc = NLP("Apple рассматривает возможность покупки стартапа из России")
    pos = [
        "PROPN",
        "VERB",
        "NOUN",
        "NOUN",
        "NOUN",
        "ADP",
        "PROPN",
    ]
    morphs = [
        "Animacy=Inan|Case=Nom|Gender=Masc|Number=Sing",
        "Aspect=Imp|Mood=Ind|Number=Sing|Person=Third|Tense=Pres|VerbForm=Fin|Voice=Act",
        "Animacy=Inan|Case=Acc|Gender=Fem|Number=Sing",
        "Animacy=Inan|Case=Gen|Gender=Fem|Number=Sing",
        "Animacy=Inan|Case=Gen|Gender=Masc|Number=Sing",
        "",
        "Animacy=Inan|Case=Gen|Gender=Fem|Number=Sing",
    ]
    for token, expected_pos, expected_morph in zip(doc, pos, morphs):
        assert token.pos_ == expected_pos
        assert str(token.morph) == expected_morph


@pytest.mark.parametrize(
    "test_file,accuracy_threshold",
    [("nerus-dev.json", 0.96)],
)
def test_ru_morphologizer_corpus(NLP, test_file, accuracy_threshold):
    data_path = TEST_FILES_DIR / test_file
    evaluate_corpus(NLP, data_path, {"morph_acc": accuracy_threshold})
    evaluate_corpus(NLP, data_path, {"pos_acc": accuracy_threshold})


def test_ru_morphologizer_spaces(NLP):
    """Ensure spaces are assigned the POS tag SPACE"""
    doc = NLP("Some\nspaces are\tnecessary.")
    assert doc[0].pos != SPACE
    assert doc[0].pos_ != "SPACE"
    assert doc[1].pos == SPACE
    assert doc[1].pos_ == "SPACE"
    assert doc[1].tag_ == "SPACE"
    assert doc[2].pos != SPACE
    assert doc[3].pos != SPACE
    assert doc[4].pos == SPACE


def test_ru_morphologizer_return_char(NLP):
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
