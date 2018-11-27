# coding: utf-8
from __future__ import unicode_literals


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
