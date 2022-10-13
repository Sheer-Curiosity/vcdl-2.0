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

linux_ffmpeg = 'https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz'
linux_ffmpeg_md5 = requests.get('https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz.md5').content.decode()[0:32]

# This is where Windows ffmpeg builds are hosted at the time of writing.
# In case this link breaks, just replace it with one to a rehost.
# Needs to be a mirror of the gyan.dev files, or else some modifications may be needed
# to this script to get it to pull the right files from the download.
win32_ffmpeg = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
win32_ffmpeg_sha256 = requests.get('https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip.sha256').content.decode()

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
	if not os.path.isfile('./ffmpeg-download.tar.xz'):
			print('[BUILD]: Downloading ffmpeg binaries (tar.xz archive)...')
			ffmpeg_dl = requests.get(linux_ffmpeg, allow_redirects=True)
			ffmpeg_dl_md5 = hashlib.md5(ffmpeg_dl.content).hexdigest()
			if ffmpeg_dl_md5 == linux_ffmpeg_md5:
				print('[BUILD]: Verified integrity of downloaded file')
				open('./ffmpeg-download.tar.xz', 'wb').write(ffmpeg_dl.content)
			else:
				print('[ERROR]: Could not verify integrity of downloaded file. Stopping build...')
				print('[INFO]: This is usually caused by a corrupted download. Retrying the build will typically\n[INFO]: fix the issue.')
				sys.exit()
	with tarfile.open('./ffmpeg-download.tar.xz', 'r:xz') as tarfileObj:
		for file in tarfileObj.getmembers():
			if file.name.endswith('ffmpeg'):
				if not os.path.isfile('./src/bin/linux/ffmpeg/ffmpeg'):
					print('[BUILD]: ffmpeg not found, retrieving...')
					open('./src/bin/linux/ffmpeg/ffmpeg', 'wb').write(tarfileObj.extractfile(file.name).read())
				else:
					print('[BUILD]: Exisiting ffmpeg file found, comparing file hashes...')
					existing_file_sha256 = hashlib.sha256()
					with open('./src/bin/linux/ffmpeg/ffmpeg', 'rb') as f:
						# Read and update hash string value in blocks of 4K
						for byte_block in iter(lambda: f.read(4096),b""):
							existing_file_sha256.update(byte_block)
					downloaded_file_sha256 = hashlib.sha256()
					with tarfileObj.extractfile(file.name) as s:
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
			if file.name.endswith('ffprobe'):
				if not os.path.isfile('./src/bin/linux/ffmpeg/ffprobe'):
					print('[BUILD]: ffprobe not found, retrieving...')
					open('./src/bin/linux/ffmpeg/ffprobe', 'wb').write(tarfileObj.extractfile(file.name).read())
				else:
					print('[BUILD]: Exisiting ffprobe file found, comparing file hashes...')
					existing_file_sha256 = hashlib.sha256()
					with open('./src/bin/linux/ffmpeg/ffprobe', 'rb') as f:
						# Read and update hash string value in blocks of 4K
						for byte_block in iter(lambda: f.read(4096),b""):
							existing_file_sha256.update(byte_block)
					downloaded_file_sha256 = hashlib.sha256()
					with tarfileObj.extractfile(file.name) as s:
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
	if os.path.isfile('./ffmpeg-download.tar.xz'):
		# Remove downloaded TAR file after extraction
		os.remove('./ffmpeg-download.tar.xz')
	
	if args.dev == True:
		PyInstaller.__main__.run([
			f"{__buildpath__}/src/main.py",
			'--add-data', f"{__buildpath__}/src/bin/linux/ffmpeg/ffmpeg:./bin/linux/ffmpeg/",
			'--specpath', f"{__buildpath__}/build/linux/development/spec/",
			'--distpath', f"{__buildpath__}/build/linux/development/bin/",
			'--workpath', f"{__buildpath__}/build/linux/development/",
			'--onefile',
			'-n', f"vcdl2_{__version__}_linux_DEV",
		])
	if args.rel == True:
		PyInstaller.__main__.run([
			f"{__buildpath__}/src/main.py",
			'--add-data', f"{__buildpath__}/src/bin/linux/ffmpeg/ffmpeg:./bin/linux/ffmpeg/",
			'--specpath', f"{__buildpath__}/build/linux/release/spec/",
			'--distpath', f"{__buildpath__}/build/linux/release/bin/",
			'--workpath', f"{__buildpath__}/build/linux/release/",
			'--onefile',
			'-n', f"vcdl2_{__version__}_linux",
		])

elif sys.platform == 'win32':
	if not os.path.isdir('./src/bin/win32/ffmpeg/'):
		os.makedirs('./src/bin/win32/ffmpeg/')
	if not os.path.isfile('./ffmpeg-download.zip'):
		# Download ZIP file with binaries if not present from previous build.
		# TODO: Add option to force redownload
		print('[BUILD]: Downloading ffmpeg binaries (zip archive)...')
		ffmpeg_dl = requests.get(win32_ffmpeg, allow_redirects=True)
		ffmpeg_dl_sha256 = hashlib.sha256(ffmpeg_dl.content).hexdigest()
		if ffmpeg_dl_sha256 == win32_ffmpeg_sha256:
			print('[BUILD]: Verified integrity of downloaded file')
			open('./ffmpeg-download.zip', 'wb').write(ffmpeg_dl.content)
		else:
			print('[ERROR]: Could not verify integrity of downloaded file. Stopping build...')
			print('[INFO]: This is usually caused by a corrupted download. Retrying the build will typically\n[INFO]: fix the issue.')
			sys.exit()
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
			'--add-data', f"{__buildpath__}/src/bin/win32/ffmpeg/ffmpeg.exe;./bin/win32/ffmpeg/",
			'--onefile',
			'--specpath', f"{__buildpath__}/build/win32/development/spec/",
			'--distpath', f"{__buildpath__}/build/win32/development/bin/",
			'--workpath', f"{__buildpath__}/build/win32/development/",
			'-n', f"vcdl2_{__version__}_win32_DEV",
		])
	if args.rel == True:
		PyInstaller.__main__.run([
			f"{__buildpath__}/src/main.py",
			'--add-data', f"{__buildpath__}/src/bin/win32/ffmpeg/ffmpeg.exe;./bin/win32/ffmpeg/",
			'--onefile',
			'--specpath', f"{__buildpath__}/build/win32/release/spec/",
			'--distpath', f"{__buildpath__}/build/win32/release/bin/",
			'--workpath', f"{__buildpath__}/build/win32/release/",
			'-n', f"vcdl2_{__version__}_win32",
		])