import os

# Tell Sphinx that it's running to avoid Firebase issues
os.environ['SPHINX_BUILD'] = '1'

import sys
sys.path.insert(0, os.path.abspath('../..'))  # Move 2 levels up to find "routes"

from firebase_admin import credentials

# Check if running in a Sphinx build
if os.getenv('SPHINX_BUILD') == '1':
    cred = None  # Skip Firebase authentication in Sphinx builds
else:
    if os.path.exists("firebase_config.json"):
        cred = credentials.Certificate("firebase_config.json")
    else:
        raise FileNotFoundError("Missing firebase_config.json file.")

# -- Project information -----------------------------------------------------
project = 'Library Management System'
copyright = '2025, Team5'
author = 'Team5'
release = '1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',      # Auto-generates documentation from docstrings
    'sphinx.ext.napoleon',     # Supports Google-style and NumPy-style docstrings
    'sphinx.ext.viewcode'      # Adds links to source code
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']
