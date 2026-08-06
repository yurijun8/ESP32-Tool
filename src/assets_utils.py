'''
This file contains utility functions for managing assets in the application. It provides a function to retrieve the absolute path to resources, 
ensuring compatibility with both development and PyInstaller environments.
'''

import sys
import os

def resource_path(relative_path):
    """ Returns the absolute path to a resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
