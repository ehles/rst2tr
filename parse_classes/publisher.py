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


class TestDocumentationTranslator(nodes.GenericNodeVisitor):
    def __init__(self, document):
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

    def default_visit(self, node):
        """Default node visit"""
        text = node.astext()
        self.output.append('[default] visit_' + node.__class__.__name__)

        self.level += 1

    def default_departure(self, node):
        """Default node departure"""
        self.level -= 1
        self.output.append('[default] departure_' + node.__class__.__name__)

    def visit_header(self, node):
        self.output.append('visit_header')

    def depart_header(self, node):
        self.output.append('departure_header')

    def visit_list_item(self, node):
        self.output.append('visit_list_item')

    def depart_list_item(self, node):
        self.output.append('departure_list_item')

    def visit_paragraph(self, node):
        self.output.append('visit_paragraph')
        self.output.append(node.astext())

    def depart_paragraph(self, node):
        self.output.append('departure_paragraph')

    def visit_Text(self, node):
        self.output.append('visit_Text')
        self.output.append(node.astext())

    def depart_Text(self, node):
        self.output.append('departure_Text')

    def visit_title(self, node):
        self.output.append('visit_title')

    def visit_section(self, node):
        self.output.append('visit_section')

    def visit_block_quote(self, node):
        self.output.append('visit_block_quote')

    def visit_enumerated_list(self, node):
        self.output.append('visit_enumerated_list')

    def depart_title(self, node):
        self.output.append('departure_title')

    def depart_section(self, node):
        self.output.append('departure_section')

    def depart_block_quote(self, node):
        self.output.append('departure_block_quote')

    def depart_enumerated_list(self, node):
        self.output.append('departure_enumerated_list')
