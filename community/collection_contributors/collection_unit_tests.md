# Add unit tests to a collection

This section describes all of the steps needed to add unit tests to a collection and how to run them locally using the `ansible-test` command.

See testing_units_modules for more details.

## Understanding the purpose of unit tests

Unit tests ensure that a section of code (known as a `unit`) meets its design requirements and behaves as intended. Some collections do not have unit tests but it does not mean they are not needed.

A `unit` is a function or method of a class used in a module or plugin. Unit tests verify that a function with a certain input returns the expected output.

Unit tests should also verify when a function raises or handles exceptions.

Ansible uses [pytest](https://docs.pytest.org/en/latest/) as a testing framework.

See testing_units_modules for complete details.

Inclusion in the Ansible package requires integration and/or unit tests You should have tests for your collection as well as for individual modules and plugins to make your code more reliable To learn how to get started with integration tests, see collection_integration_tests.

See collection_prepare_local to prepare your environment.

## Determine if unit tests exist

Ansible collection unit tests are located in the `tests/units` directory.

The structure of the unit tests matches the structure of the code base, so the tests can reside in the `tests/units/plugins/modules/` and `tests/units/plugins/module_utils` directories. There can be sub-directories if modules are organized by module groups.

If you are adding unit tests for `my_module` for example, check to see if the tests already exist in the collection source tree with the path `tests/units/plugins/modules/test_my_module.py`.

## Example of unit tests

Let's assume that the following function is in `my_module` :

``` python
def convert_to_supported(val):
    """Convert unsupported types to appropriate."""
    if isinstance(val, decimal.Decimal):
        return float(val)

    if isinstance(val, datetime.timedelta):
        return str(val)

    if val == 42:
        raise ValueError("This number is just too cool for us ;)")

    return val
```

Unit tests for this function should, at a minimum, check the following:

- If the function gets a `Decimal` argument, it returns a corresponding `float` value.
- If the function gets a `timedelta` argument, it returns a corresponding `str` value.
- If the function gets `42` as an argument, it raises a `ValueError`.
- If the function gets an argument of any other type, it does nothing and returns the same value.

To write these unit tests in collection is called `community.mycollection`:

1.  If you already have your local environment prepared, go to the collection root directory.

> ``` bash
> cd ~/ansible_collection/community/mycollection
> ```

2.  Create a test file for `my_module`. If the path does not exist, create it.

    > ``` bash
    > touch tests/units/plugins/modules/test_my_module.py
    > ```

3.  Add the following code to the file:

> ``` python
> # -*- coding: utf-8 -*-
>
> from __future__ import (absolute_import, division, print_function)
> __metaclass__ = type
>
> from datetime import timedelta
> from decimal import Decimal
>
> import pytest
>
> from ansible_collections.community.mycollection.plugins.modules.my_module import (
>     convert_to_supported,
> )
>
> # We use the @pytest.mark.parametrize decorator to parametrize the function
> # https://docs.pytest.org/en/latest/how-to/parametrize.html
> # Simply put, the first element of each tuple will be passed to
> # the test_convert_to_supported function as the test_input argument
> # and the second element of each tuple will be passed as
> # the expected argument.
> # In the function's body, we use the assert statement to check
> # if the convert_to_supported function given the test_input,
> # returns what we expect.
> @pytest.mark.parametrize('test_input, expected', [
>     (timedelta(0, 43200), '12:00:00'),
>     (Decimal('1.01'), 1.01),
>     ('string', 'string'),
>     (None, None),
>     (1, 1),
> ])
> def test_convert_to_supported(test_input, expected):
>     assert convert_to_supported(test_input) == expected
>
> def test_convert_to_supported_exception():
>     with pytest.raises(ValueError, match=r"too cool"):
>         convert_to_supported(42)
> ```
>
> See testing_units_modules for examples on how to mock `AnsibleModule` objects, monkeypatch methods (`module.fail_json`, `module.exit_json`), emulate API responses, and more.

4.  Run the tests using docker:

> ``` bash
> ansible-test units tests/unit/plugins/modules/test_my_module.py --docker
> ```

## Recommendations on coverage

Use the following tips to organize your code and test coverage:

- Make your functions simple. Small functions that do one thing with no or minimal side effects are easier to test.
- Test all possible behaviors of a function including exception related ones such as raising, catching and handling exceptions.
- When a function invokes the `module.fail_json` method, passed messages should also be checked.
