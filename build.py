from src.version import __version__

import argparse
import hashlib
import io
import os
import PyInstaller.__main__
import re
import requests
import sys
import tarfile
import zipfile

__buildpath__ = os.path.abspath('.')
print(__buildpath__)

# Damn you AV1
win32_ffmpeg = 'https://github.com/GyanD/codexffmpeg/releases/download/6.0/ffmpeg-6.0-full_build.zip'

argParser = argparse.ArgumentParser()
group = argParser.add_mutually_exclusive_group()
group.add_argument('-dev', action='store_true', help='Build VCDL2 Dev build')
group.add_argument('-rel', action='store_true', help='Build VCDL2 Release build')
args = argParser.parse_args()

if args.dev == False and args.rel == False:
	print('[ERROR]: Please specify the type of build you wish to perform (-dev, -rel)')
	sys.exit()

if sys.platform == 'linux':
	if not os.path.isdir('./src/bin/linux/ffmpeg/'):
		os.makedirs('./src/bin/linux/ffmpeg/')
	if not os.path.isfile('./src/bin/linux/ffmpeg/ffmpeg'):
		print('[BUILD/WARNING]: ffmpeg executable not found!')
		print('[BUILD/WARNING]: To build on linux, you MUST build ffmpeg yourself (https://trac.ffmpeg.org/wiki/CompilationGuide).')
		print('[BUILD/WARNING]: or find a static build with "--enable-libsvtav1"')
		print('[BUILD/WARNING]: Once finished, place the executable in the "src/bin/linux/ffmpeg" folder.')
		sys.exit()
	
	if args.dev == True:
		PyInstaller.__main__.run([
			f"{__buildpath__}/src/main.py",
			'--add-data', f"{__buildpath__}/src/bin/linux/ffmpeg/ffmpeg:./bin/ffmpeg/",
			'--specpath', f"{__buildpath__}/build/linux/development/spec/",
			'--distpath', f"{__buildpath__}/build/linux/development/bin/",
			'--workpath', f"{__buildpath__}/build/linux/development/",
			'--onefile',
			'-n', f"vcdl2_{__version__}_linux_DEV",
		])
	if args.rel == True:
		PyInstaller.__main__.run([
			f"{__buildpath__}/src/main.py",
			'--add-data', f"{__buildpath__}/src/bin/linux/ffmpeg/ffmpeg:./bin/ffmpeg/",
			'--specpath', f"{__buildpath__}/build/linux/release/spec/",
			'--distpath', f"{__buildpath__}/build/linux/release/bin/",
			'--workpath', f"{__buildpath__}/build/linux/release/",
			'--onefile',
			'-n', f"vcdl2",
		])

elif sys.platform == 'win32':
	if not os.path.isdir('./src/bin/win32/ffmpeg/'):
		os.makedirs('./src/bin/win32/ffmpeg/')
	if not os.path.isfile('./ffmpeg-download.zip'):
		# Download ZIP file with binaries if not present from previous build.
		# TODO: Add option to force redownload
		print('[BUILD]: Downloading ffmpeg binaries (zip archive)...')
		ffmpeg_dl = requests.get(win32_ffmpeg, allow_redirects=True)
		open('./ffmpeg-download.zip', 'wb').write(ffmpeg_dl.content)
	with zipfile.ZipFile('./ffmpeg-download.zip', 'r') as zipObj:
		for fileName in zipObj.namelist():
			if fileName.endswith('ffmpeg.exe'):
				if not os.path.isfile('./src/bin/win32/ffmpeg/ffmpeg.exe'):
					print('[BUILD]: ffmpeg not found, retrieving...')
					open('./src/bin/win32/ffmpeg/ffmpeg.exe', 'wb').write(zipObj.read(fileName))
				else:
					print('[BUILD]: Exisiting ffmpeg file found, comparing file hashes...')
					existing_file_sha256 = hashlib.sha256()
					with open('./src/bin/win32/ffmpeg/ffmpeg.exe', 'rb') as f:
						# Read and update hash string value in blocks of 4K
						for byte_block in iter(lambda: f.read(4096),b""):
							existing_file_sha256.update(byte_block)
					downloaded_file_sha256 = hashlib.sha256()
					with io.BytesIO(zipObj.read(fileName)) as s:
						for byte_block in iter(lambda: s.read(4096),b""):
							downloaded_file_sha256.update(byte_block)
					if (existing_file_sha256.hexdigest() != downloaded_file_sha256.hexdigest()):
						print('[BUILD]: File hashes do not match!\n[BUILD]: This usually means the downloaded file is of a newer version than the existing one.\n[BUILD]: Do you wish to replace the existing ffmpeg file with the downloaded one? [Y/n]: ', end='')
						ans = input()
						if re.search("[yY]", ans) or ans == '':
							print('[BUILD]: Using downloaded ffmpeg file')
							print('[INFO]: Passing \"--force-redownload\" will force the build to use downloaded files')
						elif re.search("[nN]", ans):
							print('[BUILD]: Using existing ffmpeg file')
							print('[INFO]: Passing \"--force-redownload\" will force the build to use downloaded files')
						else:
							print('[BUILD]: Unknown Input, assuming \"N\"')
							print('[BUILD]: Using existing ffmpeg file')
							print('[INFO]: Passing \"--force-redownload\" will force the build to use downloaded files')
					else:
						print('[BUILD]: File hashes match')
			if fileName.endswith('ffprobe.exe'):
				if not os.path.isfile('./src/bin/win32/ffmpeg/ffprobe.exe'):
					print('[BUILD]: ffprobe not found, retrieving...')
					open('./src/bin/win32/ffmpeg/ffprobe.exe', 'wb').write(zipObj.read(fileName))
				else:
					print('[BUILD]: Exisiting ffprobe file found, comparing file hashes...')
					existing_file_sha256 = hashlib.sha256()
					with open('./src/bin/win32/ffmpeg/ffprobe.exe', 'rb') as f:
						# Read and update hash string value in blocks of 4K
						for byte_block in iter(lambda: f.read(4096),b""):
							existing_file_sha256.update(byte_block)
					downloaded_file_sha256 = hashlib.sha256()
					with io.BytesIO(zipObj.read(fileName)) as s:
						for byte_block in iter(lambda: s.read(4096),b""):
							downloaded_file_sha256.update(byte_block)
					if (existing_file_sha256.hexdigest() != downloaded_file_sha256.hexdigest()):
						print('[BUILD]: File hashes do not match!\n[BUILD]: This usually means the downloaded file is of a newer version than the existing one.\n[BUILD]: Do you wish to replace the existing ffprobe file with the downloaded one? [Y/n]: ', end='')
						ans = input()
						if re.search("[yY]", ans) or ans == '':
							print('[BUILD]: Using downloaded ffprobe file')
							print('[INFO]: Passing \"--force-redownload\" will force the build to use downloaded files')
						elif re.search("[nN]", ans):
							print('[BUILD]: Using existing ffprobe file')
							print('[INFO]: Passing \"--force-redownload\" will force the build to use downloaded files')
						else:
							print('[BUILD]: Unknown Input, assuming \"N\"')
							print('[BUILD]: Using existing ffprobe file')
							print('[INFO]: Passing \"--force-redownload\" will force the build to use downloaded files')
					else:
						print('[BUILD]: File hashes match')
	if os.path.isfile('./ffmpeg-download.zip'):
		# Remove downloaded ZIP file after extraction
		os.remove('./ffmpeg-download.zip')

	if args.dev == True:
		PyInstaller.__main__.run([
			f"{__buildpath__}/src/main.py",
			'--add-data', f"{__buildpath__}/src/bin/win32/ffmpeg/ffmpeg.exe;./bin/ffmpeg/",
			'--onefile',
			'--specpath', f"{__buildpath__}/build/win32/development/spec/",
			'--distpath', f"{__buildpath__}/build/win32/development/bin/",
			'--workpath', f"{__buildpath__}/build/win32/development/",
			'-n', f"vcdl2_{__version__}_win32_DEV",
		])
	if args.rel == True:
		PyInstaller.__main__.run([
			f"{__buildpath__}/src/main.py",
			'--add-data', f"{__buildpath__}/src/bin/win32/ffmpeg/ffmpeg.exe;./bin/ffmpeg/",
			'--onefile',
			'--specpath', f"{__buildpath__}/build/win32/release/spec/",
			'--distpath', f"{__buildpath__}/build/win32/release/bin/",
			'--workpath', f"{__buildpath__}/build/win32/release/",
			'-n', f"vcdl2",
		])