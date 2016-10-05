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



class TestPersonGet:
    base_path = '/v1/person'
    people = []

    def get_url(self, server, path=None):
        path = self.base_path if path == None else path
        return '%s%s' % (server, path)

    def test_get_all_people_expect_zero(self, server):
        url = self.get_url(server, self.base_path)
        response = requests.get(url)
        self.people = json.loads(response.text)

        assert response.status_code == requests.codes.ok
        assert len(self.people) == 0

    def test_add_person(self, person, server0):
        self.people.append(person)

        url = self.get_url(server0, '{}/{}'.format(self.base_path, person['id']))
        response = requests.put(url, json=person)

        assert response.status_code == requests.codes.created

    def test_get_person(self, server, person):
        url = self.get_url(server, '{}/{}'.format(self.base_path, person['id']))
        response = requests.get(url)

        assert response.status_code == requests.codes.ok
        # Only deserialize json if response is 200
        entity = json.loads(response.text)
        # Also need to remove the reference to 'self' which isn't in the expected result
        entity.pop('self', None)
        assert entity == person

    def test_get_a_nonexistent_person(self, server):
        url = self.get_url(server, '{}/{}'.format(self.base_path, 'non-existent-user'))
        response = requests.get(url)

        assert response.status_code == requests.codes.not_found

    def test_get_all_people(self, server):
        url = self.get_url(server, self.base_path)
        response = requests.get(url)
        actual_people = json.loads(response.text)

        assert response.status_code == requests.codes.ok
        assert len(actual_people) == len(self.people)

    def test_teardown(self, server):
        for person in self.people:
            url = self.get_url(server, '{}/{}'.format(self.base_path, person['id']))
            requests.delete(url)
