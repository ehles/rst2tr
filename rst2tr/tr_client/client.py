# import urllib2, json, base64

# from functools32 import lru_cache
import requests
import logging
import base64

from helpers import timeit


class TestRailClient(object):
    user = ''
    token = ''
    def __init__(self, url, user, password):
        self._base_url = url
        self.update_token(user, password)

    def update_token(self, user, password):
        self.token = base64.b64encode('%s:%s' % (user, password))
        return self.token


    @property
    def base_url(self):
        url = self._base_url.rstrip('/')
        return '{}/index.php?/api/v2/'.format(url)

    @timeit
    def _query(self, method, url, **kwargs):
        url = self.base_url + url
        kwargs['headers'] = {
            'Content-type': 'application/json',
            'Authorization': 'Basic %s' % self.token
        }
        logging.debug('Request {0} to {1}'.format(method, url))
        response = requests.request(
            method, url, allow_redirects=False, **kwargs)
        if response.status_code >= 300:
            raise Exception(
                "Wrong response:\n"
                "status_code: {0.status_code}\n"
                "headers: {0.headers}\n"
                "content: '{0.content}'".format(response))
        result = response.json()
        if 'error' in result:
            logging.warning(result)
        return result

    def get_projects(self):
        projects = self._query('GET', 'get_projects')
        return projects

    def get_suites(self, project):
        suites = self._query('GET', 'get_suites/{0}'.format(project['id']))
        return suites

    def get_cases(self, project, **params):
        cases = self._query('GET',
                            'get_cases/{0}'.format(project['id']), params=params)
        return cases

    def get_sections(self, project, suite):
        sections = self._query('GET', 'get_sections/{0}'.format(project['id']),
                               params={'suite_id': suite['id']})
        return sections

    def find_project(self, name):
        projects = self.get_projects()
        for project in projects:
            if project['name'] == name:
                return project
        else:
            return None

    def find_suite(self, project_id, name):
        suites = self.get_suites(project_id)
        for suite in suites:
            if suite['name'] == name:
                return suite
        else:
            return None

    def find_section(self, project, suite, name):
        sections = self.get_sections(project, suite)
        for section in sections:
            if section['name'] == name:
                return section
        else:
            return None

    def add_section(self, project, suite, name):
        params = {
            'suite_id': suite['id'],
            'name': name
        }
        logging.debug('Create section project:{0}. params: {1}'.format(project['id'], params))
        section = self._query('POST',
                              'add_section/{0}'.format(project['id']),
                              json=params)
        return section

    def add_case(self, section_id, params):
        logging.debug('Create TestCase, prams: {0}'.format(params))
        case = self._query('POST',
                           'add_case/{0}'.format(section_id),
                           json=params)
        return case

    def update_case(self, case_id, params):
        logging.debug('Update TestCase, params: {0}'.format(params))
        case = self._query('POST',
                           'update_case/{0}'.format(case_id),
                           json=params)
        return case