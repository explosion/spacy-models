from pathlib import Path
from tests.util import evaluate_corpus


def test_corpus(NLP, lang, corpus_evaluation_config):
    """
    Evaluates corpus w.r.t. the specified model and language. Information on the files to use for the individual tests,
    metrics and performance thresholds are extracted from performance_thresholds.csv.
    """

    evaluate_corpus(
        NLP,
        Path(__file__).parent
        / "data"
        / "test_files"
        / lang
        / corpus_evaluation_config[0],
        {metric[0]: metric[2] for metric in corpus_evaluation_config[1]},
    )
