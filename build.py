from platform import platform
from src.utils.info import __version

import os
import PyInstaller.__main__
import requests
import sys
import zipfile

win_ffmpeg = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'

if sys.platform == 'linux':
	print()
elif sys.platform == 'win32':
	if not os.path.isdir('./src/bin/ffmpeg/'):
		os.makedirs('./src/bin/ffmpeg/')
	if not os.path.isfile('./src/bin/ffmpeg/ffmpeg.exe'):
		print('[BUILD]: ffmpeg not found. Retrieving...')
		if not os.path.isfile('./ffmpeg-download.zip'):
			ffmpeg_dl = requests.get(win_ffmpeg, allow_redirects=True)
			open('./ffmpeg-download.zip', 'wb').write(ffmpeg_dl.content)
		else:
			pass
		with zipfile.ZipFile('./ffmpeg-download.zip', 'r') as zipObj:
			listOfFileNames = zipObj.namelist()
			for fileName in listOfFileNames:
				if fileName.endswith('ffmpeg.exe'):
					open('./src/bin/ffmpeg/ffmpeg.exe', 'wb').write(zipObj.read(fileName))
	if not os.path.isfile('./src/bin/ffmpeg/ffprobe.exe'):
		print('[BUILD]: ffprobe not found. Retrieving...')
		if not os.path.isfile('./ffmpeg-download.zip'):
			ffmpeg_dl = requests.get(win_ffmpeg, allow_redirects=True)
			open('./ffmpeg-download.zip', 'wb').write(ffmpeg_dl.content)
		else:
			pass
		with zipfile.ZipFile('./ffmpeg-download.zip', 'r') as zipObj:
			listOfFileNames = zipObj.namelist()
			for fileName in listOfFileNames:
				if fileName.endswith('ffprobe.exe'):
					open('./src/bin/ffmpeg/ffprobe.exe', 'wb').write(zipObj.read(fileName))
	if not os.path.isfile('./src/bin/ffmpeg/ffplay.exe'):
		print('[BUILD]: ffplay not found. Retrieving...')
		if not os.path.isfile('./ffmpeg-download.zip'):
			ffmpeg_dl = requests.get(win_ffmpeg, allow_redirects=True)
			open('./ffmpeg-download.zip', 'wb').write(ffmpeg_dl.content)
		else:
			pass
		with zipfile.ZipFile('./ffmpeg-download.zip', 'r') as zipObj:
			listOfFileNames = zipObj.namelist()
			for fileName in listOfFileNames:
				if fileName.endswith('ffplay.exe'):
					open('./src/bin/ffmpeg/ffplay.exe', 'wb').write(zipObj.read(fileName))
	if os.path.isfile('./ffmpeg-download.zip'):
		os.remove('./ffmpeg-download.zip')

PyInstaller.__main__.run([
	'./src/main.py',
	'--add-data', './src/bin/ffmpeg/ffmpeg.exe;./bin/ffmpeg/',
	'--onefile',
	'-n', f"vcdl_{__version}",
])