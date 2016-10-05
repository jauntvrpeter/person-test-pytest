Welcome to person_tests!
=======================

Summary
-------

These are a collection of pytests for testing a fictional RESTful Person Service

Pre-requisites
--------------

- Python 2.5+ (Currently running on Python v2.7.6)
- pytest installed:

		pip install -U pytest

Running Tests
-------------

1. Open Terminal to this directory
2. Execute the following to execute all tests

		py.test

3. If you want to run specific tests, use the '-k' option

		py.test -k name_of_test_case

4. Using '-h' will bring help:

		py.test -h