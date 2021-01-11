# Russian Test Resources

The following corpora provide data for evaluating Russian models.

## Nerus

**Components:** tagger, parser

**Location:** tests/lang/ru/test_files/nerus-dev.json

**License:** CC BY-SA 4.0

### Data Preparation

1. Unfortunately there are only dev and train slices, use dev `wget https://storage.yandexcloud.net/natasha-spacy/data/nerus-dev.conllu.gz`
2. Uncompress, slice first 100 sents `gzcat nerus-dev.conllu.gz | head -1934 > nerus-dev.conllu`
3. `spacy convert nerus-dev.conllu -m -t json > nerus-dev.json`
