import pytest
from pathlib import Path
from ...util import evaluate_corpus


TEST_FILES_DIR = Path(__file__).parent / "test_files"


def test_ru_tagger_example(NLP):
    doc = NLP("Apple рассматривает возможность покупки стартапа из России")
    tags = [
        'PROPN__Animacy=Inan|Case=Nom|Gender=Masc|Number=Sing',
        'VERB__Aspect=Imp|Mood=Ind|Number=Sing|Person=Third|Tense=Pres|VerbForm=Fin|Voice=Act',
        'NOUN__Animacy=Inan|Case=Acc|Gender=Fem|Number=Sing',
        'NOUN__Animacy=Inan|Case=Gen|Gender=Fem|Number=Sing',
        'NOUN__Animacy=Inan|Case=Gen|Gender=Masc|Number=Sing',
        'ADP',
        'PROPN__Animacy=Inan|Case=Gen|Gender=Fem|Number=Sing'
    ]
    for token, expected_tag in zip(doc, tags):
        assert token.tag_ == expected_tag


@pytest.mark.parametrize(
    "test_file,accuracy_threshold",
    [("nerus-dev.json", 0.96)],
)
def test_ru_tagger_corpus(NLP, test_file, accuracy_threshold):
    data_path = TEST_FILES_DIR / test_file
    evaluate_corpus(NLP, data_path, {"tag_acc": accuracy_threshold})
