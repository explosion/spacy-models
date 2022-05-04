import pytest


@pytest.mark.skip(reason="inconsistent with lowercase augmentation?")
def test_ru_parser_example(NLP):
    doc = NLP("Apple рассматривает возможность покупки стартапа из России")
    deps = ["nsubj", "ROOT", "obj", "nmod", "nmod", "case", "nmod"]
    for token, expected_dep in zip(doc, deps):
        assert token.dep_ == expected_dep
