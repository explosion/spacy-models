import pytest
from pathlib import Path
from ...util import evaluate_corpus


TEST_FILES_DIR = Path(__file__).parent / "test_files"


@pytest.mark.parametrize(
    "test_file,lemma_threshold",
    [("fi_tdt-ud-dev001_1.json", 0.79)],
)
def test_fi_lemmatizer_corpus(NLP, test_file, lemma_threshold):
    data_path = TEST_FILES_DIR / test_file
    evaluate_corpus(
        NLP,
        data_path,
        {
            "lemma_acc": lemma_threshold,
        },
    )
