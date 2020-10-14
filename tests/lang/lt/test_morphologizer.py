import pytest
from pathlib import Path
from ...util import evaluate_corpus


TEST_FILES_DIR = Path(__file__).parent / "test_files"


@pytest.mark.parametrize(
    "test_file,pos_threshold,morph_threshold",
    [("lt_alksnis-ud-dev01_10.json", 0.86, 0.72)],
)
def test_lt_morphologizer_corpus(NLP, test_file, pos_threshold, morph_threshold):
    data_path = TEST_FILES_DIR / test_file
    evaluate_corpus(
        NLP, data_path, {"pos_acc": pos_threshold, "morph_acc": morph_threshold}
    )
