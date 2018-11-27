# coding: utf-8
from __future__ import unicode_literals


def test_de_vocab_lex_attrs(NLP):
    doc = NLP("Nettoeinkommen war 9000 $ (neuntausend). example.com")
    assert doc[0].is_title
    assert doc[1].is_stop
    assert doc[2].is_digit
    assert doc[3].is_currency
    assert doc[4].is_left_punct
    assert doc[6].is_right_punct
    assert doc[7].is_punct
    assert doc[8].like_url


def test_de_vocab_stop_words(NLP):
    doc = NLP("Dementsprechend ehrlich durfte ich zunächst später gehen")
    assert all(t.is_stop for t in doc)
