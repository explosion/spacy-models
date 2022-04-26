import collections
from pathlib import Path
from tests.util import evaluate_corpus


def test_corpus(NLP, lang, corpus_evaluation_config):
    """
    Evaluates corpus w.r.t. the specified model and language. Information on the files to use for the individual tests,
    metrics and and performance thresholds are extracted from performance_thresholds.csv.
    """

    # Ensure metric thresholds haven't been set ambiguously.
    duplicate_metrics = set()
    for key, count in collections.Counter(
        tuple(metric[0] for metric in corpus_evaluation_config[1])
    ).items():
        if count != 1:
            duplicate_metrics.add(key)
    assert (
        len(duplicate_metrics) == 0
    ), f"Metrics {duplicate_metrics} have been set more than once."

    evaluate_corpus(
        NLP,
        Path(__file__).parent
        / "data"
        / "test_files"
        / lang
        / corpus_evaluation_config[0],
        {metric[0]: metric[1] for metric in corpus_evaluation_config[1]},
    )
