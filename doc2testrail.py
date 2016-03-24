import docutils
from docutils import core
# from docutils.readers import Reader
from docutils.readers.standalone import Reader
from docutils.parsers.rst import Parser
from docutils.writers.html4css1 import Writer, HTMLTranslator

from docutils.io import StringInput

import cStringIO



def get(data):
    # ioData = cStringIO.StringIO(data)
    ioData = StringInput(source=data)
    parser = Parser()
    reader = Reader(parser=parser)
    writer = Writer()
    return reader.read(ioData, parser, None)


def foo(input_string, source_path=None, destination_path=None,
        input_encoding='unicode', doctitle=True,
        initial_header_level=1):
    from docutils import core, io
    overrides = {'input_encoding': input_encoding,
                 'doctitle_xform': doctitle,
                 'initial_header_level': initial_header_level}


    parts = core.publish_parts(
        source=input_string,
        source_path=source_path,
        destination_path=destination_path,
        writer_name='xml',
        settings_overrides=overrides)
    return parts


# def bar(data):
#     class DocParser()
#     parser = docutils.parsers.rst.Parser()
#     input = StringInput(source=data)
#     document = docutils.utils.new_document()
#     print parser.parse(input, document)