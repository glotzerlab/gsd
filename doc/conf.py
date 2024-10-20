#!/usr/bin/env python3
# Copyright (c) 2016-2024 The Regents of the University of Michigan
# Part of GSD, released under the BSD 2-Clause License.

import datetime
import os
import tempfile

import gsd

extensions = [
    'breathe',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'IPython.sphinxext.ipython_console_highlighting',
    'IPython.sphinxext.ipython_directive',
    'sphinx_copybutton',
]

if os.getenv('READTHEDOCS'):
    extensions.append('sphinxcontrib.googleanalytics')
    googleanalytics_id = 'G-25TF48HJ76'

napoleon_include_special_with_doc = True

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable', None),
    'hoomd': ('https://hoomd-blue.readthedocs.io/en/latest/', None),
}
autodoc_docstring_signature = True

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = 'GSD'
year = datetime.date.today().year
copyright = f'2016-{ year } The Regents of the University of Michigan'

version = gsd.version.version
release = version

exclude_patterns = ['_build']

default_role = 'any'

pygments_style = 'friendly'
pygments_dark_style = 'native'

html_theme = 'furo'
html_static_path = ['_static']
html_theme_options = {
    'navigation_with_keys': True,
    'top_of_page_buttons': [],
    'dark_css_variables': {
        'color-brand-primary': '#5187b2',
        'color-brand-content': '#5187b2',
    },
    'light_css_variables': {
        'color-brand-primary': '#406a8c',
        'color-brand-content': '#406a8c',
    },
}

copybutton_prompt_text = r'>>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: '
copybutton_prompt_is_regexp = True
copybutton_remove_prompts = True
copybutton_line_continuation_character = '\\'


### Add custom directives
def setup(app):
    app.add_object_type(
        'chunk', 'chunk', objname='Data chunk', indextemplate='single: %s (data chunk)'
    )


tmpdir = tempfile.TemporaryDirectory()

###### IPython directive settings
ipython_mplbackend = ''
ipython_execlines = [
    'import gsd.fl',
    'import gsd.hoomd',
    'import gsd.pygsd',
    'import numpy',
    'import os',
    f'os.chdir("{tmpdir.name}")',
]


dirname = os.path.abspath(os.path.dirname(__file__))
breathe_projects = {'gsd': os.path.join(dirname, '..', 'devdoc', 'xml')}
breathe_default_project = 'gsd'

breathe_domain_by_extension = {
    'h': 'c',
}
