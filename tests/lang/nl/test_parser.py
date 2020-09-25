import pytest
from pathlib import Path
from ...util import json_path_to_examples


TEST_FILES_DIR = Path(__file__).parent / "test_files"


@pytest.mark.parametrize(
    "test_file,uas_threshold,las_threshold",
    [("nl_lassysmall-ud-dev01_10.json", 0.82, 0.77)],
)
def test_pl_parser_corpus(NLP, test_file, uas_threshold, las_threshold):
    data_path = TEST_FILES_DIR / test_file
    if not data_path.exists():
        raise FileNotFoundError("Test corpus not found", data_path)
    examples = json_path_to_examples(data_path, NLP)
    scores = NLP.evaluate(examples)
    assert scores["dep_uas"] > uas_threshold
    assert scores["dep_las"] > las_threshold
