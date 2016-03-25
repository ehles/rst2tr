from doc2testrail import get, foo



def baz_test_parse_simple():
    from parse_classes import publisher
    from pprint import pprint

    with open('./test_doc.rst', 'r') as f:
        data = f.read()
    data = unicode(data)
    print('='*80)
    pprint(type(data))
    print('=' * 80)

    res = publisher.pub(data)
    pprint(res)



def foo_test_parse_simple():
    from parse_classes import publisher
    from pprint import pprint
    import os
    print os.getcwd()
    print os.listdir(os.getcwd())

    with open('./test_doc.rst', 'r') as f:
        data = f.read()
    res = publisher.reSTify(data)
    pprint(res)





def x_test_parse_simple():
    test = """
Test example of reST__ document.

__ http://docutils.sf.net/rst.html

- item 1
- item 2
- item 3

"""
    return get(test)


def y_test_parse_simple():
    test = u"""
Test example of reST__ document.

__ http://docutils.sf.net/rst.html

- item 1
- item 2
- item 3

"""
    print '='*80
    from pprint import pprint
    pprint(foo(test))
    print '=' * 80



def z_test_parse_simple():
    test = u"""
Test example of reST__ document.

__ http://docutils.sf.net/rst.html

- item 1
- item 2
- item 3

"""
    print '='*80
    from pprint import pprint
    pprint(bar(test))
    print '=' * 80



