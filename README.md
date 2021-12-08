# PyBryt Action

An action for running [PyBryt](https://microsoft.github.io/pybryt) as an automated assessment tool on GitHub repositories.

## Usage

The PyBryt action accepts the following inputs:

| Name | Required | Description |
|-----|-----|-----|
| `submission-path` | yes | The path to the submission file to run |
| `reference-urls` | yes | A newline-delimited list of URLs to reference implementations |
| `additional-files` | no | A newline-delimited list of file paths to also trace when executing the submission |

For example, to run PyBryt on the [Fibonacci demo in the main repo](https://github.com/microsoft/pybryt/tree/main/demo/fibonacci), you could use

```yaml
name: Run PyBryt

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Run PyBryt
        uses: chrispyles/pybryt-action@main # TODO: update the version
        with:
          submission-path: demo/fibonacci/submissions/subm01.ipynb
          reference-urls: |
            https://raw.githubusercontent.com/microsoft/pybryt/main/demo/fibonacci/fibonacci_dyn.pkl
            https://raw.githubusercontent.com/microsoft/pybryt/main/demo/fibonacci/fibonacci_map.pkl
            https://raw.githubusercontent.com/microsoft/pybryt/main/demo/fibonacci/fibonacci_no_recurse.pkl
```

If you were using a notebook as a testing harness, you may want something like:

```yaml
- name: Run PyBryt
  uses: chrispyles/pybryt-action@main # TODO: update the version
  with:
    submission-path: harness.ipynb
    additional-files: |
      student_code.py
    reference-urls: |
      https://raw.githubusercontent.com/microsoft/pybryt/main/demo/fibonacci/fibonacci_dyn.pkl
      https://raw.githubusercontent.com/microsoft/pybryt/main/demo/fibonacci/fibonacci_map.pkl
      https://raw.githubusercontent.com/microsoft/pybryt/main/demo/fibonacci/fibonacci_no_recurse.pkl
```

## Outputs

PyBryt will always print a report for each reference to the console, however it also outputs relevant artifacts into a JSON file that you can collect for further processing. The actions output is called `output-json-path` and corresponds to the path to the JSON file.

For example, you may want to commit this as a file in the student's repo:

```yaml
- name: Run PyBryt
  id: pybryt
  uses: chrispyles/pybryt-action@main # TODO: update the version
  with:
    # etc.
- name: Save, commit, and push results
  run: |
    cp ${{ steps.pybryt.outputs.output-json-path }} results.json
    git add results.json
    git commit -m "PyBryt results for ${{ github.sha }}"
    git push
```

The JSON file produced by this action has the following format:

```json
{
  "report": "the PyBryt report as a string",
  "results": "a base-64 encoded pickled list of results objects",
  "student_implementation": "a base-64 encoded pickled student implementation"
}
```

With this file, you could use a script like this to unpickle the relevant objects:

```python
import base64
import dill
import json
import pybryt

OUTPUT_JSON_PATH = ""  # fill this in with the path to the JSON file

with open(OUTPUT_JSON_PATH) as f:
    pybryt_output = json.load(f)

results: list[pybryt.ReferenceResult] = dill.loads(base64.b64decode(pybryt_output["results"].encode("utf-8")))
student_impl: pybryt.StudentImplementation = pybryt.StudentImplementation.loads(pybryt_output["student_implementation"])
```
