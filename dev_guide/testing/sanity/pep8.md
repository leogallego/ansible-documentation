# pep8

Python static analysis for PEP 8 style guideline compliance.

[PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines are enforced by [pycodestyle](https://pypi.org/project/pycodestyle/) on all python files in the repository by default.

## Running locally

The [PEP 8](https://www.python.org/dev/peps/pep-0008/) check can be run locally as follows:

``` shell
ansible-test sanity --test pep8 [file-or-directory-path-to-check] ...
```
