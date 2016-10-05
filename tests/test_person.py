#!/usr/bin/python
#
# test_person.py
#
# Author: Peter Salas
# Date of Manufacture: October 20, 2015
#
# SUMMARY
# This is an example to show pytest usage. To see accompanying test fixtures/command line arguments,
# please refer to conftest.py or do py.test -h in Terminal.


import requests
import json


# **************************************************************************************************************
# Tests
# **************************************************************************************************************


base_path = '/v1/person'

def get_url(server, path=base_path):
    return '{}{}'.format(server, path)


def test_status_code(server):
    global base_path
    url = get_url(server, base_path)
    response = requests.get(url)
    assert response.status_code == requests.codes.ok


def test_put_response(server, person):
    global base_path
    url = get_url(server, '%s/%s' % (base_path, person['id']))

    r = requests.put(url, json=person)
    assert r.status_code == 201

    url = get_url(server, '%s/%s' % (base_path, person['id']))
    r = requests.get(url)

    assert r.status_code == 200


def test_name(server, person):
    global base_path
    url = get_url(server, '%s/%s' % (base_path, person['id']))

    r = requests.get(url)
    print r.text
    entity = json.loads(r.text)

    assert person['name'] in entity['name']


def test_email(server, person):
    global base_path
    url = '%s%s/%s' % (server, base_path, person['id'])

    r = requests.get(url)
    entitys = json.loads(r.text)

    assert person['email'] in entitys['email']


def test_delete(server, person):
    global base_path
    url = get_url(server, '%s/%s' % (base_path, person['id']))

    response = requests.delete(url)

    assert response.status_code == 204
