# coding: utf-8
from __future__ import unicode_literals

import pytest
from spacy.tokens import Doc


def test_en_ner_example(NLP):
    doc = NLP("Apple is looking at buying U.K. startup for $1 billion")
    ents = [('Apple', 0, 5, 'ORG'), ('U.K.', 27, 31, 'GPE'), ('$1 billion', 44, 54, 'MONEY')]
    assert len(doc.ents) == 3
    for ent, expected in zip(doc.ents, ents):
        assert (ent.text, ent.start_char, ent.end_char, ent.label_) == expected


def test_en_ner_simple_types(NLP):
    doc = NLP("Mr. Best flew to New York on Saturday morning.")
    assert doc.ents[0].start == 1
    assert doc.ents[0].end == 2
    assert doc.ents[0].label_ == 'PERSON'
    assert doc.ents[1].start == 4
    assert doc.ents[1].end == 6
    assert doc.ents[1].label_ == 'GPE'


def test_en_ner_beam_parse(NLP):
    doc = NLP('Australia is a country', disable=['ner'])
    ner = NLP.get_pipe('ner')
    ents = ner(doc, beam_width=2)


#def test_en_ner_issue514(nlp):
#    """Test serializing after adding entity."""
#    ner = nlp.get_pipe('ner')
#    ner.add_label('FOOD')
#    doc = nlp("This is a sentence about pasta.")
#    doc.ents = [(nlp.vocab.strings['FOOD'], 5, 6)]
#    assert [(ent.label_, ent.text) for ent in doc.ents] == [("FOOD", "pasta")]
#    doc2 = Doc(nlp.vocab).from_bytes(doc.to_bytes())
#    assert [(ent.label_, ent.text) for ent in doc.ents] == [("FOOD", "pasta")]
