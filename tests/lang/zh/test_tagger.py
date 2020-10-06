import pytest
from spacy.tokens import Doc
from spacy.symbols import SPACE
from pathlib import Path
from ...util import json_path_to_examples


TEST_FILES_DIR = Path(__file__).parent / "test_files"


@pytest.mark.parametrize(
    "test_file,tag_accuracy_threshold,pos_accuracy_threshold",
    [("zh_gsd-ud-dev_sample.json", 0.29, 0.62)],
)
def test_zh_tagger_corpus(NLP, test_file, tag_accuracy_threshold, pos_accuracy_threshold):
    data_path = TEST_FILES_DIR / test_file
    if not data_path.exists():
        raise FileNotFoundError("Test corpus not found", data_path)
    examples = json_path_to_examples(data_path, NLP)
    scores = NLP.evaluate(examples)

    assert scores["tag_acc"] > tag_accuracy_threshold
    assert scores["pos_acc"] > pos_accuracy_threshold


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
