import sys
import os

def resource_path(relative_path, location):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(location)))
	return os.path.join(base_path, relative_path)