<a href="https://explosion.ai"><img src="https://explosion.ai/assets/img/logo.svg" width="125" height="125" align="right" /></a>

# spaCy model tests

This directory contains tests for spaCy's [statistical
models](https://spacy.io/models). As of spaCy `v2.1.0`, those tests will be run
automatically as part of our automated model training pipeline. They contain
both language-specific tests, regression tests, tests for known problems and
general sanity checks. You can also use this test framework to test your own
custom models and make sure they work as expected. [See
here](#contributing-tests) for details on how to contribute tests to our
official model test suite.

## Running Tests

To run the tests, clone this repository and install the test requirements. We
recommend using a [virtual
environment](https://docs.python.org/3/tutorial/venv.html) to keep your test
environment isolated and clean.

```bash
git clone https://github.com/explosion/spacy-models
cd spacy-models
```

**For older models only:** if the model is not compatible with the most recent
version of spaCy, check out the branch corresponding to the model name and
version to run the corresponding tests from when the model was published:

```bash
git checkout da_core_news_md-2.3.0
```

Next, install the test requirements and spaCy and download or install the model
to test.

```bash
pip install -r tests/requirements.txt
pip install spacy==2.3.5  # the version of spaCy to test against
# install models you want to test
python -m spacy download da_core_news_md
```

After installing the requirements, you can install one or more [spaCy
models](https://spacy.io/models) you want to test. Those can be the official
pre-trained models distributed by us, or a custom model you've trained on your
own data. You can then run the `pytest` command, set the test arguments and
point it to the `tests` directory to run all model tests:

```bash
python -m pytest tests --model en_core_web_sm --lang en --has-parser --has-tagger --has-ner
```

### Options

The following settings are available on the command line when running the tests:

| Name                  | Description                                                                                                                                                                                                                                       |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--model`             | Name of the model to test, e.g. `en_core_web_sm`. The model name will be passed directly to [`spacy.load`](https://spacy.io/api/top-level#spacy.load), so it can be the name of an installed package, a shortcut link or the path to a directory. |
| `--lang`              | The model language, e.g. `en`. This will run all language-specific tests in `/lang`, if available.                                                                                                                                                |
| `--has-vectors`       | The model has vectors. Will run all applicable vectors tests.                                                                                                                                                                                     |
| `--has-parser`        | The model has a parser. Will run all applicable parser tests.                                                                                                                                                                                     |
| `--has-tagger`        | The model has a tagger. Will run all applicable tagger tests.                                                                                                                                                                                     |
| `--has-ner`           | The model has an entity recognizer. Will run all applicable NER tests.                                                                                                                                                                            |
| `--has-morphologizer` | The model has a morphologizer. Will run all applicable morphologizer tests.                                                                                                                                                                       |
| `--has-lemmatizer`    | The model has a lemmatizer. Will run all applicable lemmatizer tests.                                                                                                                                                                             |

## Writing Tests

Tests are only run if the file name _and_ test function name is prefixed with
`test_`. Language-specific model tests are only run if the `--lang` argument set
on the command line matches the directory name. Tests for the individual
components, e.g. `test_parser.py`, are only run if the model is expected to
have those components, e.g. if `--has-parser` is set on the command line.
Alternatively, the [`pytest.mark.requires` marker](#markers) can be used to
define one or more components required for this test.

### Directory Structure

- **`/lang`** – language-specific tests, only run if `--lang` matches
  - **`/en`**
    - `test_ner.py` – only run if `--has-ner` is set
    - `test_parser.py` – only run if `--has-parser` is set
    - `test_tagger.py` – only run if `--has-tagger` is set
    - `test_vectors.py` – only run if `--has-vectors` is set
    - `test_vocab.py` – vocabulary tests
  - **`/de`**
  - _other language codes_
- `conftest.py` – pytest config and fixtures
- `test_common.py` – common tests run on all models, if applicable
- `util.py` – test utilities and helper functions

### Fixtures

The model test suite implements the following global fixtures:

| Name  | Description                                                                                                                                                                         |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `NLP` | The **session-scoped** `nlp` object with the loaded model. If you're not modifying the object, always use this one, since it will only have to be loaded once per test session.     |
| `nlp` | The **test-scoped** `nlp` object with the loaded model. If the test needs to modify the `nlp` object, using this fixture ensures that the modifications don't persist across tests. |

To use a fixture, add it to the test function's arguments:

```python
def test_common_doc_tokens(NLP):
    doc = NLP("Lorem ipsum dolor sit amet.")
    assert len(doc) > 1
```

### Markers

#### `pytest.mark.requires`

A test decorated with this marker will only be run if the model is expected
to have certain components, like `'parser'`, `'tagger'`, `'ner'` or `'vectors'`.
Note that the marker **is not needed** within test files that already specify
the component to test, like `lang/en/test_parser.py`.

```python
@pytest.mark.requires('parser', 'tagger')
def test_that_requires_tagger_and_parser(NLP):
    assert 'parser' in NLP.pipe_names
    assert 'tagger' in NLP.pipe_names
```

#### Built-in pytest markers

| Name                       | Description                                                                                                                                              |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `@pytest.mark.xfail`       | The test _currently fails_ but _should pass_.                                                                                                            |
| `@pytest.mark.skip`        | Always skip this test.                                                                                                                                   |
| `@pytest.mark.parametrize` | Run the test with different values that become available as test arguments. [See here](https://docs.pytest.org/en/latest/parametrize.html) for examples. |

## Contributing Tests

We always appreciate contributions to our test suite. However, keep in mind
that models are **statistical**, so we can't write tests for them the way we
would for a Python function. For the pre-trained models we distribute, we're
usually aiming for the best possible **compromise of accuracy, speed and file
size** for **general-purpose use cases**. This means that the models can't
_always_ be correct, especially not on difficult or ambiguous texts.

The results also always depend on the **training corpora** we have available –
so if you want to improve the pre-trained general purpose models on your text,
it's usually best to [update the models](https://spacy.io/usage/training) with
more data sepcific to your domain.

For this test suite, we're mostly looking for straightforward, non-ambiguous
sentences similar to the original training data, i.e. general news and web text
across all [available languages](https://spacy.io/models). Tests for behaviours
that most likely indicate a deeper bug with the model and the data (labels
that are not set, results that are copletely off) are also great additions.
