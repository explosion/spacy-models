# coding: utf-8
from __future__ import unicode_literals

import pytest
from spacy.gold import GoldCorpus
from pathlib import Path

TEST_FILES_DIR = Path(__file__).parent / "test_files"


@pytest.mark.parametrize(
    "test_file,ents_f_threshold",
    [("no_bokmaal-ud-dev132_1320.json",39)],
)
def test_nb_ner_corpus(NLP, test_file, ents_f_threshold):
    data_path = TEST_FILES_DIR / test_file
    if not data_path.exists():
        raise FileNotFoundError("Test corpus not found", data_path)
    corpus = GoldCorpus(data_path, data_path)
    dev_docs = list(corpus.dev_docs(NLP, gold_preproc=False))
    scorer = NLP.evaluate(dev_docs)
    assert scorer.ents_f > ents_f_threshold
