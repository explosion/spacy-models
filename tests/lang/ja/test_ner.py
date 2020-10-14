import pytest
from pathlib import Path
from ...util import evaluate_corpus


TEST_FILES_DIR = Path(__file__).parent / "test_files"


@pytest.mark.parametrize(
    "test_file,ents_f_threshold", [("ja_gsd-ud-dev_sample.json", 0.64)],
)
def test_ja_ner_corpus(NLP, test_file, ents_f_threshold):
    data_path = TEST_FILES_DIR / test_file
    evaluate_corpus(NLP, data_path, {"ents_f": ents_f_threshold})
