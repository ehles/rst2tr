from parse_classes import fsm

from pprint import pprint


def test_conf_read():
    m_reader = fsm.FSMCreator('./formats/classic.yaml')
    pprint(m_reader.conf)


def test_base_fsm_transitions():
    m_reader = fsm.FSMCreator('./formats/classic.yaml')
    machine = m_reader.get_fsm()

    for state in machine.states:
        pprint(state)

    # for transition in machine.tra