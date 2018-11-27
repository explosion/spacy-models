# coding: utf-8
from __future__ import unicode_literals

import pytest
from spacy.tokens import Doc

from ...util import apply_transition_sequence


def test_en_parser_example(NLP):
    doc = NLP("Apple is looking at buying U.K. startup")
    deps = ['nsubj', 'aux', 'ROOT', 'prep', 'pcomp', 'compound', 'dobj']
    for token, expected_dep in zip(doc, deps):
        assert token.dep_ == expected_dep


@pytest.mark.parametrize('text', ['My grandfather was laid to rest last Saturday'])
def test_en_parser_norm_exceptions(NLP, text):
    """Test that the parser isn't sensitive to different unicode variations
    that are reset in the new NORM exceptions."""
    if not NLP.vocab.vectors.size:
        text1 = '"{}"'.format(text)
        text2 = '“{}”'.format(text)
        assert [t.dep_ for t in NLP(text1)] == [t.dep_ for t in NLP(text2)]


#@pytest.mark.xfail
#def test_en_parser_sbd_serialization_projective(nlp):
#    """Test that before and after serialization, the sentence boundaries are
#    the same."""
#    text = "I bought a couch from IKEA It wasn't very comfortable."
#    transition = ['L-nsubj', 'S', 'L-det', 'R-dobj', 'D', 'R-prep', 'R-pobj',
#                  'B-ROOT', 'L-nsubj', 'R-neg', 'D', 'S', 'L-advmod',
#                  'R-acomp', 'D', 'R-punct']
#
#    doc = nlp.tokenizer(text)
#    apply_transition_sequence(nlp.get_pipe('parser'), doc, transition)
#    doc_serialized = Doc(nlp.vocab).from_bytes(doc.to_bytes())
#    assert doc.is_parsed == True
#    assert doc_serialized.is_parsed == True
#    assert doc.to_bytes() == doc_serialized.to_bytes()
#    assert [s.text for s in doc.sents] == [s.text for s in doc_serialized.sents]


def test_en_parser_issue1207(NLP):
    doc = NLP("Employees are recruiting talented staffers from overseas.")
    assert [i.text for i in doc.noun_chunks] == ['Employees', 'talented staffers']
    sent = list(doc.sents)[0]
    assert [i.text for i in sent.noun_chunks] == ['Employees', 'talented staffers']


def test_en_parser_issue693(NLP):
    """Test that doc.noun_chunks parses the complete sentence."""
    text1 = "the TopTown International Airport Board and the Goodwill Space Exploration Partnership."
    text2 = "the Goodwill Space Exploration Partnership and the TopTown International Airport Board."
    doc1 = NLP(text1)
    doc2 = NLP(text2)
    chunks1 = [chunk for chunk in doc1.noun_chunks]
    chunks2 = [chunk for chunk in doc2.noun_chunks]
    assert len(chunks1) == 2
    assert len(chunks2) == 2


@pytest.mark.xfail
def test_en_parser_issue704(NLP):
    """Test that sentence boundaries are detected correctly."""
    text = '“Atticus said to Jem one day, “I’d rather you shot at tin cans in the backyard, but I know you’ll go after birds. Shoot all the blue jays you want, if you can hit ‘em, but remember it’s a sin to kill a mockingbird.”'
    doc = NLP(text)
    assert len(list(doc.sents)) == 3


def test_en_parser_issue955(NLP):
    """Test that we don't have any nested noun chunks."""
    text = "Does flight number three fifty-four require a connecting flight to get to Boston?"
    doc = NLP(text)
    seen_tokens = set()
    for np in doc.noun_chunks:
        for word in np:
            key = (word.i, word.text)
            assert key not in seen_tokens
            seen_tokens.add(key)


@pytest.mark.skip
@pytest.mark.parametrize('text,expected_sents', [
    pytest.param("Hello World. My name is Jonas.", ["Hello World.", "My name is Jonas."], marks=pytest.mark.xfail()),
    ("What is your name? My name is Jonas.", ["What is your name?", "My name is Jonas."]),
    ("There it is! I found it.", ["There it is!", "I found it."]),
    ("My name is Jonas E. Smith.", ["My name is Jonas E. Smith."]),
    ("Please turn to p. 55.", ["Please turn to p. 55."]),
    ("Were Jane and co. at the party?", ["Were Jane and co. at the party?"]),
    ("They closed the deal with Pitt, Briggs & Co. at noon.", ["They closed the deal with Pitt, Briggs & Co. at noon."]),
    ("Let's ask Jane and co. They should know.", ["Let's ask Jane and co.", "They should know."]),
    ("They closed the deal with Pitt, Briggs & Co. It closed yesterday.", ["They closed the deal with Pitt, Briggs & Co.", "It closed yesterday."]),
    ("I can see Mt. Fuji from here.", ["I can see Mt. Fuji from here."]),
    pytest.param("St. Michael's Church is on 5th st. near the light.", ["St. Michael's Church is on 5th st. near the light."], marks=pytest.mark.xfail()),
    ("That is JFK Jr.'s book.", ["That is JFK Jr.'s book."]),
    ("I visited the U.S.A. last year.", ["I visited the U.S.A. last year."]),
    ("I live in the E.U. How about you?", ["I live in the E.U.", "How about you?"]),
    ("I live in the U.S. How about you?", ["I live in the U.S.", "How about you?"]),
    ("I work for the U.S. Government in Virginia.", ["I work for the U.S. Government in Virginia."]),
    ("I have lived in the U.S. for 20 years.", ["I have lived in the U.S. for 20 years."]),
    pytest.param("At 5 a.m. Mr. Smith went to the bank. He left the bank at 6 P.M. Mr. Smith then went to the store.", ["At 5 a.m. Mr. Smith went to the bank.", "He left the bank at 6 P.M.", "Mr. Smith then went to the store."], marks=pytest.mark.xfail()),
    ("She has $100.00 in her bag.", ["She has $100.00 in her bag."]),
    ("She has $100.00. It is in her bag.", ["She has $100.00.", "It is in her bag."]),
    ("He teaches science (He previously worked for 5 years as an engineer.) at the local University.", ["He teaches science (He previously worked for 5 years as an engineer.) at the local University."]),
    ("Her email is Jane.Doe@example.com. I sent her an email.", ["Her email is Jane.Doe@example.com.", "I sent her an email."]),
    ("The site is: https://www.example.50.com/new-site/awesome_content.html. Please check it out.", ["The site is: https://www.example.50.com/new-site/awesome_content.html.", "Please check it out."]),
    pytest.param("She turned to him, 'This is great.' she said.", ["She turned to him, 'This is great.' she said."], marks=pytest.mark.xfail()),
    pytest.param('She turned to him, "This is great." she said.', ['She turned to him, "This is great." she said.'], marks=pytest.mark.xfail()),
    ('She turned to him, "This is great." She held the book out to show him.', ['She turned to him, "This is great."', "She held the book out to show him."]),
    ("Hello!! Long time no see.", ["Hello!!", "Long time no see."]),
    ("Hello?? Who is there?", ["Hello??", "Who is there?"]),
    ("Hello!? Is that you?", ["Hello!?", "Is that you?"]),
    ("Hello?! Is that you?", ["Hello?!", "Is that you?"]),
    pytest.param("1.) The first item 2.) The second item", ["1.) The first item", "2.) The second item"], marks=pytest.mark.xfail()),
    pytest.param("1.) The first item. 2.) The second item.", ["1.) The first item.", "2.) The second item."], marks=pytest.mark.xfail()),
    pytest.param("1) The first item 2) The second item", ["1) The first item", "2) The second item"], marks=pytest.mark.xfail()),
    ("1) The first item. 2) The second item.", ["1) The first item.", "2) The second item."]),
    pytest.param("1. The first item 2. The second item", ["1. The first item", "2. The second item"], marks=pytest.mark.xfail()),
    pytest.param("1. The first item. 2. The second item.", ["1. The first item.", "2. The second item."], marks=pytest.mark.xfail()),
    pytest.param("• 9. The first item • 10. The second item", ["• 9. The first item", "• 10. The second item"], marks=pytest.mark.xfail()),
    pytest.param("⁃9. The first item ⁃10. The second item", ["⁃9. The first item", "⁃10. The second item"], marks=pytest.mark.xfail()),
    pytest.param("a. The first item b. The second item c. The third list item", ["a. The first item", "b. The second item", "c. The third list item"], marks=pytest.mark.xfail()),
    ("This is a sentence\ncut off in the middle because pdf.", ["This is a sentence\ncut off in the middle because pdf."]),
    ("It was a cold \nnight in the city.", ["It was a cold \nnight in the city."]),
    pytest.param("features\ncontact manager\nevents, activities\n", ["features", "contact manager", "events, activities"], marks=pytest.mark.xfail()),
    pytest.param("You can find it at N°. 1026.253.553. That is where the treasure is.", ["You can find it at N°. 1026.253.553.", "That is where the treasure is."], marks=pytest.mark.xfail()),
    ("She works at Yahoo! in the accounting department.", ["She works at Yahoo! in the accounting department."]),
    ("We make a good team, you and I. Did you see Albert I. Jones yesterday?", ["We make a good team, you and I.", "Did you see Albert I. Jones yesterday?"]),
    ("Thoreau argues that by simplifying one’s life, “the laws of the universe will appear less complex. . . .”", ["Thoreau argues that by simplifying one’s life, “the laws of the universe will appear less complex. . . .”"]),
    pytest.param(""""Bohr [...] used the analogy of parallel stairways [...]" (Smith 55).""", ['"Bohr [...] used the analogy of parallel stairways [...]" (Smith 55).'], marks=pytest.mark.xfail()),
    ("If words are left off at the end of a sentence, and that is all that is omitted, indicate the omission with ellipsis marks (preceded and followed by a space) and then indicate the end of the sentence with a period . . . . Next sentence.", ["If words are left off at the end of a sentence, and that is all that is omitted, indicate the omission with ellipsis marks (preceded and followed by a space) and then indicate the end of the sentence with a period . . . .", "Next sentence."]),
    ("I never meant that.... She left the store.", ["I never meant that....", "She left the store."]),
    pytest.param("I wasn’t really ... well, what I mean...see . . . what I'm saying, the thing is . . . I didn’t mean it.", ["I wasn’t really ... well, what I mean...see . . . what I'm saying, the thing is . . . I didn’t mean it."], marks=pytest.mark.xfail()),
    pytest.param("One further habit which was somewhat weakened . . . was that of combining words into self-interpreting compounds. . . . The practice was not abandoned. . . .", ["One further habit which was somewhat weakened . . . was that of combining words into self-interpreting compounds.", ". . . The practice was not abandoned. . . ."], marks=pytest.mark.xfail()),
    pytest.param("Hello world.Today is Tuesday.Mr. Smith went to the store and bought 1,000.That is a lot.", ["Hello world.", "Today is Tuesday.", "Mr. Smith went to the store and bought 1,000.", "That is a lot."], marks=pytest.mark.xfail())
])
def test_en_sbd_prag(NLP, text, expected_sents):
    """SBD tests from Pragmatic Segmenter"""
    doc = NLP(text)
    sents = []
    for sent in doc.sents:
        sents.append(''.join(doc[i].string for i in range(sent.start, sent.end)).strip())
    assert sents == expected_sents
