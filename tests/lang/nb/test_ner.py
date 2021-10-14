import pytest
from pathlib import Path
from ...util import evaluate_corpus


TEST_FILES_DIR = Path(__file__).parent / "test_files"


@pytest.mark.parametrize(
    "test_file,ents_f_threshold", [("no_bokmaal-ud-dev132_1320.json", 0.70)],
)
def test_nb_ner_corpus(NLP, test_file, ents_f_threshold):
    data_path = TEST_FILES_DIR / test_file
    evaluate_corpus(NLP, data_path, {"ents_f": ents_f_threshold})
