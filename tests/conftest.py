#!/usr/bin/python
#
# conftest.py
#
# Author: Peter Salas
# Date of Manufacture: October 20, 2015
#
# SUMMARY
# Configuration file for custom configurations for test_example. This will automatically get run before
# test_example.py when pytest is run via command line.

import pytest


# **************************************************************************************************************
# COMMAND LINE ARGS
# **************************************************************************************************************


def pytest_addoption(parser):
    """
    pytest convention to create sysargv-style command line options
    """
    ## These are not used, but are examples of what you could do
    parser.addoption("--protocol", action="append", default=["http"], help="Specify http protocol")
    parser.addoption("--host", action="append", default=["localhost"], help="Specify host to test")
    parser.addoption("--port", action="append", default=["8080"], help="Specify host's port")

    ## This is ultimately used for the tests
    parser.addoption("--server", action="append", default=['http://localhost:8080'],
                     help="Specify the Person Service uri (e.g. http://localhost:8080)")


def pytest_generate_tests(metafunc):
    """
    This is pytest convention to create custom dynamic parametrization schemes
    """
    if 'protocol' in metafunc.fixturenames:
        metafunc.parametrize("protocol", metafunc.config.option.protocol)

    if 'host' in metafunc.fixturenames:
        metafunc.parametrize("host", metafunc.config.option.host)

    if 'port' in metafunc.fixturenames:
        metafunc.parametrize("port", metafunc.config.option.port)

    if 'base_url' in metafunc.fixturenames:
        base_url = []
        tmp_list = metafunc.config.option.protocol + metafunc.config.option.host + metafunc.config.option.port
        base_url.append("".join(tmp_list))
        metafunc.parametrize("base_url", base_url)

    if 'server' in metafunc.fixturenames:
        metafunc.parametrize("server", metafunc.config.option.server)

    # Also create 'n' fixtures with just 1 server each
    for index in xrange(len(metafunc.config.option.server)):
        if 'server{}'.format(index) in metafunc.fixturenames:
            metafunc.parametrize('server{}'.format(index), [metafunc.config.option.server[index]])


# **************************************************************************************************************
# FIXTURES
# **************************************************************************************************************


@pytest.fixture(params=["/v1/person"])
def path(request):
    return request.param


@pytest.fixture(params=['alice'])
def id(request):
    return request.param


@pytest.fixture(params=['Alice N. Wonderland'])
def name(request):
    return request.param

@pytest.fixture(
    params=[{'id': 'alice', 'name': "Alice", 'email': "alice@proofpoint.com"}],
    ids=['alice']
)
def person(request):
    return request.param


@pytest.fixture(params=['alice@proofpoint.com'])
def email(request):
    return request.param

