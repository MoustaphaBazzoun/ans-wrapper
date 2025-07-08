# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os

sys.path.insert(0, os.path.abspath('../../src'))


project = 'ANS-Wrapper'
copyright = '2025, Mousta Bazzoun'
author = 'Mousta Bazzoun'
release = '0.1.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
  "sphinx.ext.autodoc",
  "sphinx.ext.napoleon",
  "sphinx_autodoc_typehints",
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
#html_theme = 'sphinx_rtd_theme'
#html_theme = "pydata_sphinx_theme"
#html_theme = "sphinx_orange_book_theme"
#html_theme = "shibuya"

html_static_path = ['_static']

#pygments_style = "gruvbox-dark"  # or "gruvbox-light"

# Optional but useful to customize Napoleon
napoleon_google_docstring = True
napoleon_numpy_docstring = False