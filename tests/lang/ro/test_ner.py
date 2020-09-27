import pytest
from pathlib import Path
from ...util import json_path_to_examples


TEST_FILES_DIR = Path(__file__).parent / "test_files"


@pytest.mark.parametrize(
    "test_file,ents_f_threshold",
    [("dev_ronec01_10.json", 0.79)],
)
def test_ro_ner_corpus(NLP, test_file, ents_f_threshold):
    data_path = TEST_FILES_DIR / test_file
    if not data_path.exists():
        raise FileNotFoundError("Test corpus not found", data_path)
    examples = json_path_to_examples(data_path, NLP)
    scores = NLP.evaluate(examples)

    assert scores["ents_f"] > ents_f_threshold
