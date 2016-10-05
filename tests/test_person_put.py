#!/usr/bin/python
#
# test_person_get.py
#
# Author: Peter Salas
# Date of Manufacture: October 20, 2015
#
# SUMMARY
# This is an example to show pytest usage. To see accompanying test fixtures/command line arguments,
# please refer to conftest.py or do py.test -h in Terminal.

from __future__ import print_function
import requests
import json
import pytest


# **************************************************************************************************************
# Tests
# **************************************************************************************************************



class TestPersonPut:
    base_path = '/v1/person'
    people = []
    delete_server = None

    def get_url(self, server, path=None):
        path = self.base_path if path == None else path
        return '%s%s' % (server, path)

    def teardown_method(self, method):
        print(" executing teardown_method : {}")
        for person in self.people:
            if self.delete_server:
                url = self.get_url(self.delete_server, '{}/{}'.format(self.base_path, person['id']))
                requests.delete(url)
        self.delete_server = None

    def test_add_a_user(self, server, person):
        self.people.append(person)
        self.delete_server = server

        url = self.get_url(server, '{}/{}'.format(self.base_path, person['id']))
        response = requests.put(url, json=person)
        assert response.status_code == requests.codes.created

    def test_add_a_user_idempotency(self, server, person):
        self.people.append(person)
        self.delete_server = server

        ## First request
        url = self.get_url(server, '{}/{}'.format(self.base_path, person['id']))
        response = requests.put(url, json=person)
        assert response.status_code == requests.codes.created

        ## Second request
        response = requests.put(url, json=person)
        assert response.status_code == requests.codes.created

    def test_update_a_user(self, server, person):
        self.people.append(person)
        self.delete_server = server
        change_name = 'foobar'

        ## Insert person
        url = self.get_url(server, '{}/{}'.format(self.base_path, person['id']))
        response = requests.put(url, json=person)
        assert response.status_code == requests.codes.created

        ## Update content
        person['name'] = change_name
        response = requests.put(url, json=person)
        assert response.status_code == requests.codes.no_content

        ## Verify with a GET
        url = self.get_url(server, '{}/{}'.format(self.base_path, person['id']))
        response = requests.get(url, json=person)
        entity = json.loads(response.text)
        assert response.status_code == requests.codes.ok
        assert entity['name'] == change_name

    def test_add_a_user_with_mismatched_id(self, server, person):
        self.people.append(person)
        self.delete_server = server

        url = self.get_url(server, '{}/{}'.format(self.base_path, 'foobar'))
        response = requests.put(url, json=person)
        assert response.status_code == requests.codes.bad_request
