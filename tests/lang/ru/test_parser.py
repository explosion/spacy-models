import pytest
from pathlib import Path
from ...util import evaluate_corpus


TEST_FILES_DIR = Path(__file__).parent / "test_files"


def test_ru_parser_example(NLP):
    doc = NLP("Apple рассматривает возможность покупки стартапа из России")
    deps = ['nsubj', 'ROOT', 'obj', 'nmod', 'nmod', 'case', 'nmod']
    for token, expected_dep in zip(doc, deps):
        assert token.dep_ == expected_dep


@pytest.mark.parametrize(
    "test_file,uas_threshold,las_threshold",
    [("nerus-dev.json", 0.95, 0.90)],
)
def test_ru_parser_corpus(NLP, test_file, uas_threshold, las_threshold):
    data_path = TEST_FILES_DIR / test_file
    evaluate_corpus(
        NLP, data_path, {"dep_uas": uas_threshold, "dep_las": las_threshold}
    )
