import yaml
from transitions import Machine


class FSMCreator(object):
    def __init__(self, filename):
        self.conf = self.load_conf(filename)

    @classmethod
    def load_conf(cls, filename):
        with open(filename, 'r') as fstream:
            try:
                return yaml.load(fstream)
            except yaml.YAMLError as exc:
                print("Error reading machine configuration file: '%s'" % exc)
                return None

    def get_fsm_old(self):
        reader = FormatReader()

        states = self.conf['document_sections']
        states.extend(self.conf['case_sections'])
        initial = states[0]
        transitions = [
            {'trigger': 't_section', 'source': 'document', 'dest': 'title'},
            {'trigger': 't_section', 'source': 'document', 'dest': 'title'},
        ]
        machine = Machine(model=reader,
                          states=states,
                          transitions=transitions,
                          initial=initial)
        return machine

    def get_fsm(self):
        reader = FormatReader()

        states = ['start', 'suite', 'case', 'section', 'step']
        initial = states[0]
        transitions = [
            {'trigger': 't_section', 'source': 'document', 'dest': 'title'},
            {'trigger': 't_section', 'source': 'document', 'dest': 'title'},
            {'trigger': 't_step', 'source': 'section', 'dest': 'step'},
        ]
        machine = Machine(model=reader,
                          states=states,
                          transitions=transitions,
                          initial=initial)
        graph = machine.get_graph()
        graph.draw('fsm.png', prog='dot')
        return machine

class FormatReader(object):
    pass