import logging

class Step:
    index = -1  # some invalid value for checking
    description = ''
    expected = ''

    def __init__(self, description, expected=None):
        self.description = description
        if expected is not None:
            self.expected = expected

    def show(self):
        return self.description, self.expected


class Case:
    case_id = ''
    title = ''
    description = ''
    complexity = ''
    expected = ''
    steps = []

    def __init__(self, title):
        self.title = title
        self.steps = []

    def add_step(self, step):
        step.index = len(self.steps)
        self.steps.append(step)

    def show(self):
        return {
            'id': self.case_id,
            'titile': self.title,
            'description': self.description,
            'complexity': self.complexity,
            'expected': self.expected,
            'steps': [step.show() for step in self.steps]
        }


class Suite:
    title = ''
    cases = []

    def __init__(self, title):
        self.cases = []
        self.title = title

    def add_case(self, case):
        self.cases.append(case)

    def show(self):
        return {
            'title': self.title,
            'cases': [case.show() for case in self.cases]
        }


class Constructor:

    def __init__(self):
        self.suites = []
        self.current_suite = None
        self.current_case = None
        self.current_step = None
        self.last_item = None

    def show(self):
        return {
            'suites': [suite.show() for suite in self.suites]
        }

    def add_element(self, element, value):
        if element == 'suite_title':
            # Store current suite and create new one
            self.current_suite = Suite(title=value)
            self.suites.append(self.current_suite)
        elif element == 'case_title':
            case = Case(title=value)
            self.current_case = case
            self.current_suite.add_case(case)
        elif element in ['case_id',
                         'case_description',
                         'case_complexity',
                         'case_expected_results']:
            self.last_item = element
        elif element == 'case_single_step':
            step = Step(description=value)
            self.current_step = step
            self.current_case.add_step(step)
        elif element == 'item_value':
            if self.last_item == 'case_id':
                self.current_case.case_id = value
            elif self.last_item == 'case_description':
                self.current_case.description = value
            elif self.last_item == 'case_complexity':
                self.current_case.complexity = value
            elif self.last_item == 'case_expected_results':
                self.current_case.expected = value
            else:
                # logging.warning("Unknown item '{0}': {1} = {2}".format(self.last_item,
                #                                                        element,
                #                                                        value))
                raise Exception("Unknown item '{0}': {1} = {2}".format(self.last_item,
                                                                       element,
                                                                       value))
            self.last_item = None
        elif element == 'noop':
            logging.debug("No operation")

