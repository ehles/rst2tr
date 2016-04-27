#!/usr/bin/env python

import re
import os
import yaml
import logging
from parse_classes import processor

from helpers import timeit
from getopts import Opts
from tr_client.client import TestRailClient


def setup_logger(loglevel=logging.INFO):
    FORMAT = '[%(asctime)-15s][%(levelname)-8s] %(message)s'
    logging.basicConfig(format=FORMAT, level=loglevel)

@timeit
def process():
    command_args = Opts()
    if command_args.options.verbose:
        setup_logger(logging.DEBUG)
    else:
        setup_logger()
    logging.debug("Command options: {0}".format(command_args.options))
    logging.debug("Command args: {0}".format(command_args.args))
    logging.debug("Command env: {0}".format(command_args.env))
    suites = []
    if command_args.options.doc_file is not None:
        suites.extend(parse(command_args.options.doc_file, command_args.options.format_file))
    if command_args.options.doc_dir is not None:
        re_obj = re.compile(r'test_suite_.*.rst$')
        doc_dir = command_args.options.doc_dir
        for f in os.listdir(doc_dir):
            filename = os.path.join(doc_dir, f)
            if os.path.isfile(filename):
                if re_obj.match(f):
                    suites.extend(parse(filename, command_args.options.format_file))

    upload_test_data(command_args.env['testrail'], suites)

@timeit
def parse(rst_filename, format_filename):
    logging.info('Parse test documentation file "{0}", format file "{1}'.format(rst_filename, format_filename))
    with open(rst_filename, 'r') as f:
        data = f.read()
    data = unicode(data, errors='ignore')
    with open(format_filename, 'r') as dtf:
        doc_tree = yaml.safe_load(dtf)
    res = processor.process_single_doc(data, doc_tree['model'])
    logging.debug("Suites: {0}".format(res.show()))
    return res.suites


def add_case(tr, section, doc_case):
    logging.debug('Add TestCase "{0}"'.format(doc_case.title))
    case_params = {
        # 'section_id': '',
        'title': doc_case.title,
        # 'template_id': '',
        # 'type_id': '',
        # 'priority_id':'',
        # 'estimate':'',
        # 'milestone_id':''
        'test_case_description': doc_case.description,
    }
    steps = []
    for step in doc_case.steps:
        steps.append({
            'content': step.description,
            'expected': doc_case.expected,
        })
    customs = {
        'custom_test_group': doc_case.case_id,
        'custom_steps_separated': steps
    }
    tr.add_case(section['id'], dict(case_params, **customs))

def update_case(tr, doc_case, tr_case):
    logging.debug('Update TestCase "{0}"'.format(doc_case.title))
    case_params = {
        # 'section_id': '', # Section is not supported by update
        'title': doc_case.title,
        # 'template_id': '',
        # 'type_id': '',
        # 'priority_id':'',
        # 'estimate':'',
        # 'milestone_id':''
    }
    steps = []
    for step in doc_case.steps:
        steps.append({
            'content': step.description,
            'expected': doc_case.expected,
        })
    customs = {
        'custom_test_group': doc_case.case_id,
        'custom_steps_separated': steps,
        'custom_test_case_description': doc_case.description,
    }
    tr.update_case(tr_case['id'], dict(case_params, **customs))

def upload_test_data(testrail_conf, sections):
    logging.info('Upload test scenarios.')
    for suite in sections:
        logging.debug("TestSuite: {0}".format(suite.title))
        for case in suite.cases:
            logging.debug("TestCase: {0}; expected: {1}".format(case.title, case.expected))
            for step in case.steps:
                logging.debug("TestStep: {0}; expected: {1}".format(step.description, step.expected))

    tclient = TestRailClient(testrail_conf['url'],
                             testrail_conf['user'],
                             testrail_conf['api_key'])

    ####################################################################################################################
    # tr_project = tclient.find_project(testrail_conf['project'])
    # tr_suite = tclient.find_suite(tr_project, testrail_conf['suite'])
    # if not tr_suite:
    #     Exception('Suite {} not found.'.format(testrail_conf['suite']))
    ####################################################################################################################

    tr_project = tclient.find_project(testrail_conf['project'])
    if testrail_conf['suite']:
        tr_suite = tclient.find_suite(tr_project, testrail_conf['suite'])
        if not tr_suite:
            raise Exception('Suite "{}" not found in TestRail.'.format(testrail_conf['suite']))

        # Find TestCases
        for doc_section in sections:
            tr_section = tclient.find_section(tr_project, tr_suite, doc_section.title)
            if not tr_section:
                if testrail_conf['create_section']:
                    logging.info('Create section "{0}'.format(doc_section.title))
                    tr_section = tclient.add_section(tr_project, tr_suite, doc_section.title)
                else:
                    raise Exception('Section "{0}" not found'.format(doc_section.title))
            logging.info('Process section: {}'.format(doc_section.title))
            for doc_case in doc_section.cases:
                tr_cases = tclient.get_cases(tr_project, suite_id=tr_suite['id'])
                for tr_case in tr_cases:
                    if doc_case.case_id == tr_case['custom_test_group']:
                        logging.info('TestCase "{0}" found'.format(doc_case.case_id))
                        update_case(tclient, doc_case, tr_case)
                        break
                else:
                    logging.info('TestCase "{0}" not found in TestRail, create.'.format(doc_case.case_id))
                    add_case(tclient, tr_section, doc_case)


if __name__ == '__main__':
    process()
    # upload_test_data(None)

