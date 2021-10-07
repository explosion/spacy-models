import pytest


@pytest.mark.parametrize(
    "word,morph",
    [
        ("綜合", ("ソウゴウ", "")),
        ("縁側", ("エンガワ", "")),
        ("新しい", ("アタラシイ", "形容詞;終止形-一般")),
        ("新しくない", ("アタラシク", "形容詞;連用形-一般")),
        ("やった", ("ヤッ", "五段-ラ行;連用形-促音便")),
        ("せよ", ("セヨ", "サ行変格;命令形")),
    ],
)
def test_ja_morph(NLP, word, morph):
    doc = NLP(word)
    reading, infl = morph

    assert reading == doc[0].morph.get("reading")[0]
    assert infl.split(",") == doc[0].morph.get("inflection")
