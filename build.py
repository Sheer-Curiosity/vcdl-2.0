from src.version import __version__

import os
import PyInstaller.__main__
import requests
import sys
import zipfile

# This is where official Windows ffmpeg builds are hosted at the time of writing.
# In case this link breaks, just replace it with one to a rehost.
win_ffmpeg = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'

if sys.platform == 'linux':
	print()
elif sys.platform == 'win32':
	if not os.path.isdir('./src/bin/ffmpeg/'):
		os.makedirs('./src/bin/ffmpeg/')
	if not os.path.isfile('./src/bin/ffmpeg/ffmpeg.exe'):
		print('[BUILD]: ffmpeg not found. Retrieving...')
		if not os.path.isfile('./ffmpeg-download.zip'):
			# Download ZIP file with binaries if not present from previous build.
			# TODO: Add option to force redownload
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
			# Download ZIP file with binaries if not present from previous build.
			# TODO: Line 21
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
			# Download ZIP file with binaries if not present from previous build.
			# TODO: Line 21
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
		# Remove downloaded ZIP file after extraction
		os.remove('./ffmpeg-download.zip')

PyInstaller.__main__.run([
	'./src/main.py',
	'--add-data', './src/bin/ffmpeg/ffmpeg.exe;./bin/ffmpeg/',
	'--onefile',
	'-n', f"vcdl_{__version__}",
])