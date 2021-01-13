import pytest
from pathlib import Path
from ...util import evaluate_corpus


TEST_FILES_DIR = Path(__file__).parent / "test_files"


@pytest.mark.parametrize(
    "test_file,uas_threshold,las_threshold",
    [("lt_alksnis-ud-dev01_10.json", 0.60, 0.52)],
)
def test_lt_parser_corpus(NLP, test_file, uas_threshold, las_threshold):
    data_path = TEST_FILES_DIR / test_file
    evaluate_corpus(
        NLP, data_path, {"dep_uas": uas_threshold, "dep_las": las_threshold}
    )
