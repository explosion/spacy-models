import pytest


def test_en_vocab_lex_attrs(NLP):
    doc = NLP("Net income was $9 (nine) million. example.com")
    assert doc[0].is_title
    assert doc[1].is_lower
    assert doc[2].is_stop
    assert doc[3].is_currency
    assert doc[4].is_digit
    assert doc[5].is_left_punct
    assert doc[6].like_num
    assert doc[7].is_right_punct
    assert doc[9].is_punct
    assert doc[10].like_url


def test_en_vocab_stop_words(NLP):
    doc = NLP("I was indeed very into her")
    assert all(t.is_stop for t in doc)


@pytest.mark.xfail
@pytest.mark.requires("vectors")
@pytest.mark.parametrize("word", ["number", "mark", "root", "agent"])
def test_issue2461(NLP, word):
    """Test that special symbols that are also common words are in vocab."""
    assert word in NLP.vocab
