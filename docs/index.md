# Overview

This project tries to implement an end to end python repository following [12 factor app methodology](https://12factor.net/) that includes CI/CD pipeline using **Github Actions**, code quality tools integration like ruff, mypy, uv and mkdocs for documentation using docstrings and typing within project source code.

Also, the template project is a REST API using FastAPI framework that implements a basic calculator. Pytest is used for unit and integration tests.

For full source code of this project please visit [repo template](https://github.com/joagonzalez/python-seed/).

## How to use this repo
Please check how to use this repository in the repo [README](https://github.com/joagonzalez/python-seed/blob/master/README.md) file

## Open issues
Please check open issues at [github](https://github.com/joagonzalez/python-seed/issues)

## Changelog

[v0.0.1]
- Documentation migrated to readthedocs service
- Dynamic badges for coverage (github acions), documentation as stated before, build status (github actions)
- API basic unit tests added
- ruff and mypy for linting and static analysis
- uv for packet management
- basic tests with pytest