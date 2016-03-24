from docutils import core
from docutils.writers.html4css1 import Writer, HTMLTranslator
from docutils import writers
from docutils.readers.standalone import Reader
from docutils.parsers.rst import Parser

from docutils import io


class NoHeaderHTMLTranslator(HTMLTranslator):
    def __init__(self, document):
        HTMLTranslator.__init__(self, document)
        self.head_prefix = ['','','','','']
        self.body_prefix = []
        self.body_suffix = []
        self.stylesheet = []


class Publisher(core.Publisher):
    pass


class TRWriter(writers.Writer):
    supported = ('pprint', 'pformat', 'pseudoxml')
    """Formats this writer supports."""

    config_section = 'pseudoxml writer'
    config_section_dependencies = ('writers',)

    output = None
    """Final translated form of `document`."""

    def translate(self):
        self.output = self.document.pformat()

    def supports(self, format):
        """This writer supports all format-specific elements."""
        return True


def reSTify(s):
    return Publisher().publish(s)


def pub(s):
    reader = None
    parser = None
    writer = None
    pub = Publisher(reader,
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
    pub.set_source(source=s, source_path=None)
    pub.set_destination(destination=None, destination_path=None)
    output = pub.publish(enable_exit_status=False)
    return output, pub

if __name__ == '__main__':
    test = """
Test example of reST__ document.

__ http://docutils.sf.net/rst.html

- item 1
- item 2
- item 3

"""
    print reSTify(test)
