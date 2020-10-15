import pytest
from spacy.tokens import Doc
from pathlib import Path
from ...util import evaluate_corpus


TEST_FILES_DIR = Path(__file__).parent / "test_files"


@pytest.mark.parametrize(
    "test_file,accuracy_threshold", [("ja_gsd-ud-dev_sample.json", 0.96)],
)
def test_ja_segmenter_corpus(NLP, test_file, accuracy_threshold):
    data_path = TEST_FILES_DIR / test_file
    evaluate_corpus(NLP, data_path, {"token_acc": accuracy_threshold})
