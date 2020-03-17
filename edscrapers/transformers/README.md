# ED Transformers

This module is used to take the data dumped by scrapers and model it into
formats usable by other applications.


## Structure

A transformer submodule has the following mandatory structure:

- a new directory under `transformers`
- a `__init__.py` file within the new path
- a `transformer.py` file in the new path
  - exposing a `transform(name, in_file_path)` function definition
    - `name` is a scraper name
    - `in_file_path` is a file name used as a input


## Input

By default, the transformers will loop through all the scraping output. There
are, however, two modifiers to that behaviour:

- specifying a `name` parameter to act on (i.e. a name of a scraper pipeline,
  such as `edgov`)
- specifying a `in_file_path` parameter to loop through a list of paths instead
  og globbing the directories
  

## Output

Default output is in `<ED_OUTPUT_DIR>/transformers/<TRANSFORMER_NAME>/`.
