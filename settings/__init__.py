"""
Common configuration settings.
Attempts to import `.local.py` as the effective project configuration.
"""
from __future__ import absolute_import, print_function

try:
    from .local import *
    print('local.py imported')
except ImportError:
    from .common import *
