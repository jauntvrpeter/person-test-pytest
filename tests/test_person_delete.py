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



class TestPersonDelete:
    base_path = '/v1/person'
    people_ids = []

    def get_url(self, server, path=None):
        path = self.base_path if path == None else path
        return '%s%s' % (server, path)


    def add_person(self, server, person):
        if person['id'] not in self.people_ids:
            self.people_ids.append(person)

        url = self.get_url(server, '{}/{}'.format(self.base_path, person['id']))
        response = requests.put(url, json=person)
        assert response.status_code == requests.codes.created

    def test_delete_a_person(self, server, person):
        self.add_person(server, person)

        url = self.get_url(server, '{}/{}'.format(self.base_path, person['id']))
        response = requests.delete(url)
        assert response.status_code == requests.codes.no_content

    def test_delete_a_person_idempotent(self, server, person):
        self.add_person(server, person)

        url = self.get_url(server, '{}/{}'.format(self.base_path, person['id']))
        response = requests.delete(url)
        assert response.status_code == requests.codes.no_content
        response = requests.delete(url)
        assert response.status_code == requests.codes.no_content

    def test_delete_nonexistent_person(self, server):
        url = self.get_url(server, '{}/{}'.format(self.base_path, 'foobar'))
        response = requests.delete(url)
        assert response.status_code == requests.codes.not_found

    def test_teardown_class(self, server0):
        print(" cleaning up any mess")
        for person_id in self.people_ids:
            url = self.get_url(server0, '{}/{}'.format(self.base_path, person_id))
            requests.delete(url)
