import pytest


def test_ru_ner_example(NLP):
    doc = NLP("Apple рассматривает возможность покупки стартапа из России за $1 млрд")
    ents = [("Apple", 0, 5, "ORG"), ("России", 52, 58, "LOC")]
    assert len(doc.ents) == 2
    for ent, expected in zip(doc.ents, ents):
        assert (ent.text, ent.start_char, ent.end_char, ent.label_) == expected
