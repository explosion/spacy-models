# English Test Resources

The following corpora provide data for evaluating English models.

## MASC

**Components:** tagger, parser

**Location:** tests/lang/en/test_files/masc-penn-treebank-sample.json

A sample of 5% of sentences (2050 sentences) from the
[MASC](https://www.anc.org/data/masc/) (Manually Annotated Sub-Corpus) from the
Open American National Corpus. It contains a variety of written genres: blog,
email, essays, ficlets, fiction, govt-docs, jokes, journal, letters,
movie-script, newspaper, non-fiction, technical, travel-guides, twitter.

**License:** CC-BY 3.0

**Citation:**

```
@inproceedings{ide-etal-2008-masc,
    title = "{MASC}: the Manually Annotated Sub-Corpus of {A}merican {E}nglish",
    author = "Ide, Nancy  and
      Baker, Collin  and
      Fellbaum, Christiane  and
      Fillmore, Charles  and
      Passonneau, Rebecca",
    booktitle = "LREC 2008",
    year = "2008",
    url = "http://www.lrec-conf.org/proceedings/lrec2008/pdf/617_paper.pdf",
}
```

### Data Preparation

1. The files in `penn-treebank/data/written` were converted with
[ClearNLP](https://github.com/clir/clearnlp) using the converter
`edu.emory.clir.clearnlp.bin.C2DConvert` with the options:

    ```
    -r -i /path/to/masc/penn-treebank/data/written -h /path/to/headrule_en_stanford.txt -pe mrg
    ```

    (The file `blog/sucker.mrg` couldn't be converted and was skipped.)

1. Initial `<begin_.*>` marker sentences (present only in the Penn Treebank
annotation and not in the main MASC corpus) were removed.

1. CoNLL-X was converted to CoNLL-U and 5% of sentences were selected 
randomly.

1. CoNLL-U was converted using `spacy convert -t json`.

### Performance

Because of the differences in genres between OntoNotes and MASC, the 
performance is lower than for news/web text.

en_core_web_sm 2.1.0:

```
POS       88.37 
UAS       82.93 
LAS       79.11 
```

en_core_web_md 2.1.0:

```
POS       89.19 
UAS       83.35 
LAS       79.89 
```

en_core_web_lg 2.1.0:

```
POS       89.59 
UAS       83.88 
LAS       80.48 

```

## Parallel Universal Dependencies (PUD) English Treebank

**Components:** tagger

**Location:** tests/lang/en/test_files/en_pud-ud-test.json

The [English PUD test 
corpus](https://github.com/UniversalDependencies/UD_English-PUD) v2.4, which
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

1. `spacy convert en_pud-ud-test.conllu -t json`

### Performance

The genres are more similar to OntoNotes, so performance is higher than for
MASC.

en_core_web_sm 2.1.0:

```
POS       94.47
```

en_core_web_md 2.1.0:

```
POS       94.85
```

en_core_web_lg 2.1.0:

```
POS       95.17
```
