# German Test Resources

The following corpora provide data for evaluating German models.

There are very few German resources (corpora or models) that are freely 
available for use in a commercial context, so the evaluation and tests 
are currently rather limited.

## Parallel Universal Dependencies (PUD) German Treebank

**Components:** tagger, parser (minimal)

**Location:** tests/lang/de/test_files/de_pud-ud-test.stts.json

**Description:** The [German PUD test
corpus](https://github.com/UniversalDependencies/UD_German-PUD) v2.4, which
contains news and Wikipedia data (1000 sentences).

**License:** CC BY-SA 3.0

**Citation:**

```
Nivre, Joakim; Abrams, Mitchell; Agić, Željko; et al., 2019, Universal
Dependencies 2.4, LINDAT/CLARIN digital library at the Institute of Formal and
Applied Linguistics (ÚFAL), Faculty of Mathematics and Physics, Charles
University, http://hdl.handle.net/11234/1-2988.
```

### Data Preparation

1. The expanded multiword tokens such as (`zur` -> `zu`, `dem`) were removed,
leaving only the original token from the text (`zur`).

1. The texts were tagged with spacy 2.0 and 2.1 (de_core_news_sm, 2.0.0,
de_core_news_md, 2.1.0).

1. Heuristic rules were applied that took into account the available tags: UD
tags, fine-grained tags (which appears to be from a Google internal tagset?),
and the two spacy tags.

    Common ambiguous cases where the UD tag maps unambiguously back to STTS rely
on the gold UD/Google tags, which appear to be more more accurate than the
automatic spacy tags: verb forms (VVINF vs. VVFIN vs. VVPP), ART vs. PRELS, NE
vs. NN, ADV vs. ADJD, etc.

    The UD PUNCT tags for non-ASCII punctuation are mapped to the appropriate
STTS tag (typically `$(`, since it's mainly non-ASCII punctuation where spacy,
especially spacy 2.1, has problems).

    In the remaining cases, if the two spacy tags agree, the spacy STTS tag is
used. If the spacy tags do not agree, then the UD/Google tags (and rarely the
token itself) are used to choose between the two spacy tags.

    Finally, a handful of cases where the spacy tags disagreed were corrected 
    by hand.

Some problems and inconsistencies remain. There are definitely inconsistencies
related to:

* poor tokenization in the original corpus

    * compounds split on "-" (there are no STTS tags for the non-final 
      elements of compounds)

    * abbreviations such as `z . B.`, `bzw .`

    * ordinals such as `1.` tokenized as `1 .` in some instances

* foreign language material (in UD_German-PUD typically tagged with the correct
  POS for the foreign material rather than with FM)

### Performance

de_core_news_sm 2.0.0:

```
POS       94.57
```

de_core_news_sm 2.1.0:

```
POS       93.36
```

de_core_news_md 2.1.0:

```
POS       94.02
```
