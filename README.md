# rst2tr

Upload test documentation from reStructured to TestRail

Documentation formats
---------------------
Currently prepared 'classic' and 'modern' formats:
* [Classic](tests/data/classic.rst)
* [Modern](tests/data/modern.rst)

to add new documenstation format you should prepare *model-file* for them. There are model-files:
* [Classic-model](formats/classic_model.yaml)
* [Modern-model](formats/modern_model.yaml)

Usage
-----
```
rst2tr.py -f formats/classic_model.yaml -d tests/data/classic.rst -v -s tests/data/tests/
```
Command line parameters:
* -v, --verbose - Enable debug output
* -f, --format-file - Test documentation model-file
* -d, --doc-file - Test documentation .rst file
* -s, --doc-dir - Test documentation directory which contains suite of .rst files
* -n, --noop - Only check documentation formatting without pushing got the remote.

You could use both or one of -d and -s options.

Environment parameters:
* TESTRAIL_URL - TestRail URL
* TESTRAIL_USER - TestRail user's email
* TESTRAIL_API_key - TestRail user's password or API-key
* TESTRAIL_PROJECT - Project name
* TESTRAIL_MILESTONE - Milestone name
* TESTRAIL_SUITE - Suite name
* TESTRAIL_CUSTOM_QA_TEAM - Custom case field row id for QA Team.
* TESTRAIL_CREATE_SECTION - Create absent section or raise exception.
