# DesignSafe Jobs

[![PyTest](https://github.com/geoelements/dsjobs/actions/workflows/pytest.yml/badge.svg)](https://github.com/geoelements/dsjobs/actions/workflows/lint-test.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.md)

`dsjobs` is a library that simplifies the process of submitting, running, and monitoring [TAPIS v2 / AgavePy](https://agavepy.readthedocs.io/en/latest/index.html) jobs on [DesignSafe](https://designsafe-ci.org) via [Jupyter Notebooks](https://jupyter.designsafe-ci.org).

## Installation

Install `dsjobs` via pip (**coming soon**)

```shell
pip3 install dsjobs
```

To install the current development version of the library use:

```shell
pip install git+https://github.com/geoelements/dsjobs.git --quiet
```

## Features

* Simplified TAPIS v2 Calls: No need to fiddle with complex API requests. `dsjobs` abstracts away the complexities.

* Seamless Integration with DesignSafe Jupyter Notebooks: Launch DesignSafe applications directly from the Jupyter environment.

## Support

For any questions, issues, or feedback submit an [issue](https://github.com/geoelements/dsjobs/issues/new)

## Development

To develop or test the library locally. Install [Poetry](https://python-poetry.org/docs/#installation). In the current repository run the following commands

```shell
poetry shell
poetry install
poetry build
```

To run the unit test
```shell
poetry run pytest -v
```

## License

`dsjobs` is licensed under the [MIT License](LICENSE.md).

## Authors

* Prof. Pedro Arduino, University of Washington
* Krishna Kumar, University of Texas at Austin