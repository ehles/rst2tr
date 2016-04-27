# from parse_classes import processor
from pprint import pprint

from docutils import io
from docutils import core

# from docutils import core
# from docutils.writers.html4css1 import Writer, HTMLTranslator
# from docutils import writers
# from docutils.readers.standalone import Reader
# from docutils.parsers.rst import Parser
from docutils import writers, nodes, frontend


class TRWriter(writers.Writer):
    supported = ('pprint', 'pformat', 'testrail')
    """Formats this writer supports."""

    config_section = 'testrail writer'
    config_section_dependencies = ('writers',)

    output = None
    visitor = None
    """Final translated form of `document`."""

    def __init__(self):
        writers.Writer.__init__(self)
        self.translation_class = TestDocumentationTranslator

    def translate(self):
        self.visitor = self.translation_class(self.document)
        self.document.walkabout(self.visitor)
        self.output = self.visitor.output

        from pprint import pprint
        pprint(self.output)

    def supports(self, format):
        """This writer supports all format-specific elements."""
        return True



format = {
  'suite_title':            {'path': 'document.title.Text'},
  'case_title':             {'path': 'section.title.Text'},
  'case_id':                {'path': 'section.title.Text', 'kw': 'ID'},
  'case_description':       {'path': 'section.title.Text', 'kw': 'Description'},
  'case_complexity':        {'path': 'section.title.Text', 'kw': 'Complexity'},
  'case_expected_results':  {'path': 'section.title.Text', 'kw': 'Expected results'},
  'case_steps':             {'path': 'section.block_quote.enumerated_list', 'kw': 'Steps'},
}

tree = {
    'section': {
        'title': {
            'Text': [
                {'item': 'case_title'},
                {'item': 'case_id', 'kw': 'ID'},
                {'item': 'case_description', 'kw': 'Description'},
                {'item': 'case_complexity', 'kw': 'Complexity'},
                {'item': 'case_expected_results', 'kw': 'Expected results'}]},
        'block_quote': {
            'enumerated_list':[
                {'item': 'case_steps', 'kw': 'Steps'}]}
    },
    'document': {
        'title': {
            'Text': [
                {'item': 'suite_title'},
            ]
        }
    },
}


class TestDocumentationTranslator(nodes.GenericNodeVisitor):
    def __init__(self, document, document_tree):
        nodes.NodeVisitor.__init__(self, document)

        # Reporter
        self.warn = self.document.reporter.warning
        self.error = self.document.reporter.error

        # Settings
        self.settings = settings = document.settings
        self.indent = self.newline = ''
        # if settings.newlines:
        #     self.newline = '\n'
        # if settings.indents:
        #     self.newline = '\n'
        #     self.indent = '    '
        self.level = 0  # indentation level
        self.in_simple = 0  # level of nesting inside mixed-content elements

        self.output = []

        self.document_tree = document_tree
        self.curr_path = ''
        self.curr_subtree = document_tree

    def default_visit(self, node):
        """Default node visit"""
        text = node.astext()
        curr_node_name = node.__class__.__name__
        self.output.append('[default] visit_' + curr_node_name)
        curr_branch_path = '{0}.{1}'.format(self.curr_path, curr_node_name)
        curr_subtree_keys = self.curr_subtree.keys()
        if curr_node_name in curr_subtree_keys:
            new_subtree = self.curr_subtree.get(curr_node_name, None)
            if type(new_subtree) is list:
                # check value
                print('Branch: {}'.format(curr_branch_path))
                for item in new_subtree:
                    if text == item.get('kw', None):
                        print("Found: {0} = {1}".format(item['item'], text))
                        break
                else:
                    # FIXME: do NOT go over this list again
                    for item in new_subtree:
                        if item.get('kw', None) is None:
                            print("Found: {0} == {1}".format(item['item'], text))
                            break
                    else:
                        print("Unknown tree path: {}".format(curr_branch_path))
                        # Reset tree paths
                        self.curr_path = ''
                        self.curr_subtree = self.document_tree
                        self.level = 0
            else:
                # check subtree again
                self.curr_subtree = new_subtree
                self.curr_path = curr_branch_path
                self.level += 1
        else:
            # Unknown branch
            print("Unknown branch: {}".format(curr_branch_path))
            self.curr_path = ''
            self.curr_subtree = self.document_tree
            self.level = 0

    def default_departure(self, node):
        """Default node departure"""
        def get_node(tree, path):
            result_node = tree
            for step in path.split('.'):
                if step:
                    curr_position = tree.get(step, None)
                    if curr_position:
                        result_node = curr_position
                    else:
                        return result_node
            return result_node

        self.level -= 1
        self.output.append('[default] departure_' + node.__class__.__name__)
        self.curr_path = '.'.join(self.curr_path.split('.')[:-1])
        self.curr_subtree = get_node(self.document_tree, self.curr_path)

    # def visit_header(self, node):
    #     self.output.append('visit_header')
    #
    # def depart_header(self, node):
    #     self.output.append('departure_header')
    #
    # def visit_list_item(self, node):
    #     self.output.append('visit_list_item')
    #
    # def depart_list_item(self, node):
    #     self.output.append('departure_list_item')
    #
    # def visit_paragraph(self, node):
    #     self.output.append('visit_paragraph')
    #     self.output.append(node.astext())
    #
    # def depart_paragraph(self, node):
    #     self.output.append('departure_paragraph')
    #
    # def visit_Text(self, node):
    #     self.output.append('visit_Text')
    #     self.output.append(node.astext())
    #
    # def depart_Text(self, node):
    #     self.output.append('departure_Text')
    #
    # def visit_title(self, node):
    #     self.output.append('visit_title')
    #
    # def visit_section(self, node):
    #     self.output.append('visit_section')
    #
    # def visit_block_quote(self, node):
    #     self.output.append('visit_block_quote')
    #
    # def visit_enumerated_list(self, node):
    #     self.output.append('visit_enumerated_list')
    #
    # def depart_title(self, node):
    #     self.output.append('departure_title')
    #
    # def depart_section(self, node):
    #     self.output.append('departure_section')
    #
    # def depart_block_quote(self, node):
    #     self.output.append('departure_block_quote')
    #
    # def depart_enumerated_list(self, node):
    #     self.output.append('departure_enumerated_list')


def parse_simple(filename, format_filename):
    with open(filename, 'r') as f:
        data = f.read()
    data = unicode(data)
    print('='*80)
    pprint(type(data))
    print('=' * 80)

    res = process_single_doc(data)
    pprint(res)


def process_single_doc(doc_string):
    reader = None
    parser = None
    writer = None
    pub = core.Publisher(reader,
                         parser,
                         writer=TRWriter(),
                         settings=None,
                         source_class=io.StringInput,
                         destination_class=io.StringOutput)
    pub.set_components(reader_name='standalone',
                       parser_name='restructuredtext',
                       writer_name='pseudoxml')
    settings = {
        'input_encoding': 'unicode',
        'doctitle_xform': True,
        'initial_header_level': 1,
        'tab_width': 4,
    }
    pub.process_programmatic_settings(settings_spec=None,
                                      settings_overrides=settings,
                                      config_section=None)
    pub.set_source(source=doc_string, source_path=None)
    pub.set_destination(destination=None, destination_path=None)
    output = pub.publish(enable_exit_status=False)
    return output, pub


if __name__ == '__main__':
    parse_simple('tests/data/modern.rst', 'formats/modern.yaml')