import os
from optparse import OptionParser


class Opts(object):
    def __init__(self):
        self.get_env()
        self.get_opts()

    def get_opts(self):
        self.__parser = OptionParser(description="Upload tests cases to TestRail. ")

        self.__parser.add_option("-v", "--verbose",
                                 action="store_true", dest="verbose", default=False,
                                 help="Enable debug output")
        self.__parser.add_option("-n", "--noop",
                                 action="store_true", dest="noop", default=False,
                                 help="Only parse documentation without pushing to the server")
        self.__parser.add_option('-f', '--format-file', dest='format_file', default=None,
                                 help='Test documentation file format description.')
        self.__parser.add_option('-d', '--doc-file', dest='doc_file',
                                 default=None,
                                 help='Test documentation .rst file')
        self.__parser.add_option('-s', '--doc-dir', dest='doc_dir', default=None,
                                 help='Test documentation directory which contains suite of .rst files')
        self.__options, self.__args = self.__parser.parse_args()

    def get_env(self):
        self.__env_opts = {
            'testrail': {
                'url': os.getenv('TESTRAIL_URL', ''),
                'user': os.getenv('TESTRAIL_USER', ''),
                'api_key': os.getenv('TESTRAIL_API_KEY', ''),
                'project': os.getenv('TESTRAIL_PROJECT', ''),
                'suite': os.getenv('TESTRAIL_SUITE', ''),
                'milestone': os.getenv('TESTRAIL_MILESTONE', ''),

                'create_section': os.getenv('TESTRAIL_CREATE_SECTION', True),

                'custom_qa_team': os.getenv('TESTRAIL_CUSTOM_QA_TEAM', ''),
            }
        }

    @property
    def env(self):
        return self.__env_opts

    @property
    def options(self):
        return self.__options

    @property
    def args(self):
        return self.__args
