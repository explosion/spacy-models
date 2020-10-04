import srsly
from spacy.tokens import DocBin
from spacy.training import Example
from spacy.training.converters import json_to_docs


def json_path_to_examples(data_path, NLP):
    data = srsly.read_json(data_path)
    # no good way to convert with a specified vocab, so convert, then reload
    # through DocBin with the right vocab
    docs = json_to_docs(data)
    docbin = DocBin()
    for doc in docs:
        docbin.add(doc)
    docs = docbin.get_docs(NLP.vocab)
    examples = [Example(NLP.make_doc(doc.text), doc) for doc in docs]
    return examples


def apply_transition_sequence(parser, doc, sequence):
    """Perform a series of pre-specified transitions, to put the parser in a
    desired state."""
    for action_name in sequence:
        if "-" in action_name:
            move, label = action_name.split("-")
            parser.add_label(label)
    with parser.step_through(doc) as stepwise:
        for transition in sequence:
            stepwise.transition(transition)
