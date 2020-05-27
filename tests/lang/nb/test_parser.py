# coding: utf-8
from __future__ import unicode_literals

import pytest
from spacy.gold import GoldCorpus
from pathlib import Path
from ...util import apply_transition_sequence


TEST_FILES_DIR = Path(__file__).parent / "test_files"


@pytest.mark.parametrize(
    "test_file,uas_threshold,las_threshold",
    [("no_bokmaal-ud-dev132_1320.json", 74, 72)],
)
def test_nb_parser_corpus(NLP, test_file, uas_threshold, las_threshold):
    data_path = TEST_FILES_DIR / test_file
    if not data_path.exists():
        raise FileNotFoundError("Test corpus not found", data_path)
    corpus = GoldCorpus(data_path, data_path)
    dev_docs = list(corpus.dev_docs(NLP, gold_preproc=False))
    scorer = NLP.evaluate(dev_docs)
    assert scorer.uas > uas_threshold
    assert scorer.las > las_threshold
