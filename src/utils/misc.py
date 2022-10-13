import sys
import os

def resource_path(build_path, location):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	if getattr(sys, 'frozen', False):
		base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(location)))
		return os.path.join(base_path, build_path)
	else:
		if sys.platform == 'win32': dev_path = 'bin/win32/ffmpeg/ffmpeg'
		if sys.platform == 'linux': dev_path = 'bin/linux/ffmpeg/ffmpeg'
		base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(location)))
		return os.path.join(base_path, dev_path)
