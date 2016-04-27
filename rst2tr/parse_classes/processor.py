from docutils import io
from docutils import core

from . import publisher


def process_single_doc(doc_string, doc_tree):
    reader = None
    parser = None
    writer = None
    pub = core.Publisher(reader,
                         parser,
                         writer=publisher.TRWriter(doc_tree),
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
    return output
