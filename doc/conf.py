#!/usr/bin/env python3
# Copyright (c) 2016-2021 The Regents of the University of Michigan
# Part of GSD, released under the BSD 2-Clause License.

import sys
import os
import gsd
import datetime

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'IPython.sphinxext.ipython_console_highlighting',
    'IPython.sphinxext.ipython_directive'
]

intersphinx_mapping = {'python': ('https://docs.python.org/3', None), 'numpy': ('https://docs.scipy.org/doc/numpy', None)}
autodoc_docstring_signature = True;

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = 'GSD'
year = datetime.date.today().year
copyright = f'2016-{ year } The Regents of the University of Michigan'

version = gsd.__version__
release = version

exclude_patterns = ['_build']

default_role = 'any'

pygments_style = 'sphinx'

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = [
    'css/gsd-theme.css',
]
### Add custom directives
def setup(app):
    app.add_object_type('chunk', 'chunk',
                        objname='Data chunk',
                        indextemplate='single: %s (data chunk)')

###### IPython directive settings
ipython_mplbackend = ''
ipython_execlines = ['import gsd.fl', 'import gsd.hoomd', 'import gsd.pygsd', 'import numpy']
