import pytest
from pathlib import Path
from ...util import json_path_to_examples


TEST_FILES_DIR = Path(__file__).parent / "test_files"


@pytest.mark.parametrize("test_file", [("de_pud-ud-test.stts.json")])
def test_de_parser_depset(NLP, test_file):
    """Check that no tags outside the tagset are used."""
    # fmt: off
    gold_deps = set(["ROOT", "ac", "adc", "ag", "ams", "app", "avc", "cc", "cd",
                     "cj", "cm", "cp", "cvc", "da", "dm", "ep", "ju", "mnr",
                     "mo", "ng", "nk", "nmc", "oa", "oc", "og", "op", "par",
                     "pd", "pg", "ph", "pm", "pnc", "punct", "rc", "re", "rs",
                     "sb", "sbp", "sp", "svp", "uc", "vo",
                     # The 'dep' label is introduced by the frequency cutoff
                     # during projectivisation. So we still need this, even
                     # though it doesn't occur in the gold data.
                     "dep"
                     ])
    # fmt: on
    data_path = TEST_FILES_DIR / test_file
    if not data_path.exists():
        raise FileNotFoundError("Test corpus not found", data_path)
    examples = json_path_to_examples(data_path, NLP)
    pred_deps = set()
    parser = NLP.get_pipe("parser")
    for example in examples:
        doc = example.predicted
        parser(doc)
        pred_deps = pred_deps.union(set([t.dep_ for t in doc]))
    unexpected_labels = pred_deps - gold_deps
    assert not unexpected_labels
