# coding: utf-8
from __future__ import unicode_literals

import pytest


@pytest.mark.xfail
def test_fr_tagger_issue2251(NLP):
    doc = NLP("Tu vas bien.")
    assert doc[0].tag_ == 'PRON__Number=Sing|Person=2'
    doc = NLP("Comment vas-tu?")
    print(doc[3].tag_, doc[3].lemma_)
    assert doc[3].tag_ == 'PRON__Number=Sing|Person=2'
    assert doc[3].lemma_ == 'tu'


@pytest.mark.xfail
def test_fr_tagger_issue1958(NLP):
    doc = NLP("Pour poser des congés, qu'est-ce que je fais ?")
    assert all(t.pos != 0 for t in doc)
    assert all(t.pos_ for t in doc)
    assert all(t.tag != 0 for t in doc)
    assert all(t.tag_ for t in doc)
