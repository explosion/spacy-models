import pytest
from spacy.tokens import Doc
from spacy.symbols import SPACE
from pathlib import Path


TEST_FILES_DIR = Path(__file__).parent / "test_files"


@pytest.mark.parametrize(
    "test_file,accuracy_threshold",
    [("zh_gsd-ud-dev_sample.json", 0.70)],
)
def test_zh_segmenter_corpus(NLP, test_file, accuracy_threshold):
    data_path = TEST_FILES_DIR / test_file
    if not data_path.exists():
        raise FileNotFoundError("Test corpus not found", data_path)
    examples = json_path_to_examples(data_path, NLP)
    scores = NLP.evaluate(examples)

    assert scores["token_acc"] > accuracy_threshold
