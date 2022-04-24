def test_corpus(NLP, corpus_evaluation_configs):
    """
    Evaluates corpus w.r.t. the specified model and language. Information on the files to use for the individual tests,
    metrics and and performance thresholds are extracted from performance_thresholds.csv.
    """

    # Extract parameter sets for evaluate_corpus() calls.
    print(corpus_evaluation_configs)
    # print(extract_corpus_evaluation_configs(lang, model_size))
    # print(test_file, threshold)
    assert 0 == 1

