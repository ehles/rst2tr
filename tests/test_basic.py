from parse_classes import processor
from pprint import pprint


def test_parse_simple():
    with open('./data/modern.rst', 'r') as f:
        data = f.read()
    data = unicode(data)
    print('='*80)
    pprint(type(data))
    print('=' * 80)

    res = processor.process_single_doc(data)
    pprint(res)
