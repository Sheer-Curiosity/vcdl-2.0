# I did not use pyton to code this by choice. I absolutely hate python. It doesn't make sense to me when I read it, and in my opinion
# using indents as syntax is the most idiotic thing ever. But, it was the most suitable language to solve the problem I have, and thus
# my hand is forced.
#
# Reluctantly written by Sheer Curiosity

from clipper.merger import mergeClips
from clipper.extractor import getAVUrls
from clipper.downloader import *
from clipper.misc import *
from utils.info import *
from utils.misc import *

import argparse
import os
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import sys

class MainWindow(QWidget):

	# 0: link(s)
	# 1: timestamps
	# 2: output name
	# 3: padding
	# 4: download method
	# 5: output merged
	# 6: output archive
	# 7: cookie file
	info = ['','','','','','','','']

	def __init__(self):
		super().__init__()

		self.initUI()

	def initUI(self):

		linksLabel = QLabel('Video Link(s)')
		linksLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)
		self.links = QLineEdit()

		timestampsLabel = QLabel('Timestamps')
		timestampsLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)
		self.timestamps = QLineEdit()

		outputNameLabel = QLabel('Output Name')
		outputNameLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)
		self.outputName = QLineEdit('Output')

		downloadButtonIcon = QIcon()
		downloadButtonIcon.addFile(gui_resource_path('gui/icons/download.svg', os.path.abspath(__file__)))
		downloadButton = QPushButton()
		downloadButton.setIcon(downloadButtonIcon)
		downloadButton.setIconSize(QSize(30, 40))
		downloadButton.clicked.connect(self.assignAndVerifyInput)

		cookieFileLabel = QLabel('Netscape Cookie File')
		cookieFileLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)
		cookieFileButton = QPushButton()
		cookieFileButton.setText('Browse...')
		cookieFileButton.setFixedWidth(80)
		cookieFileButton.clicked.connect(self.getCookieFile)

		self.dlMethodDropdown = QComboBox()
		self.dlMethodDropdown.setFixedWidth(100)
		self.dlMethodDropdown.setLayoutDirection()
		self.dlMethodDropdown.addItems(['DPAMRE', 'DWACFF'])
		self.dlMethodDropdown.setPlaceholderText('Select...')
		self.dlMethodDropdown.setCurrentIndex(-1)

		gbDetails = QGroupBox('Info')

		gbGrid = QGridLayout()
		gbGrid.setHorizontalSpacing(10)
		gbGrid.setVerticalSpacing(0)
		gbDetails.setLayout(gbGrid)

		gbGrid.addWidget(linksLabel, 0, 0)
		gbGrid.addWidget(self.links, 0, 1)

		gbGrid.addWidget(timestampsLabel, 1, 0)
		gbGrid.addWidget(self.timestamps, 1, 1)

		gbGrid.addWidget(outputNameLabel, 2, 0)
		gbGrid.addWidget(self.outputName, 2, 1)

		gbGrid.addWidget(cookieFileLabel, 3, 0)

		br1 = QGridLayout()
		br1.addWidget(cookieFileButton, 0, 0)
		br1.addWidget(self.dlMethodDropdown, 0, 1)

		gbGrid.addLayout(br1, 3, 1)

		gbGrid.addWidget(downloadButton, 4, 0)

		grid = QGridLayout()
		grid.setSpacing(10)
		self.setLayout(grid)

		grid.addWidget(gbDetails)

		self.setGeometry(300, 300, 700, 400)
		self.setWindowTitle('VCDL2')
		self.show()
	
	def getCookieFile(self):
		fileName = QFileDialog.getOpenFileName(self,'Single File','C:\'','*.txt')
		if fileName[0] == '':
			return
		else:
			self.info[7] = fileName[0]

	def assignAndVerifyInput(self):
		info = self.info
		info = [self.links.text(), 
		  self.timestamps.text(), 
		  self.outputName.text(),
		  ]
		


		

ffmpeg_path = ffmpeg_resource_path('bin/ffmpeg/ffmpeg', os.path.abspath(__file__))
tempdir_parent_path = '.'

argParser = argparse.ArgumentParser(prog='tool', formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=120), usage="vcdl2 -v [VIDEO LINKS] -ts [TIMESTAMPS] [options]")
argParser.add_argument('-v', '--video-links', nargs='*', help='link(s) to download from')
argParser.add_argument('-ts', '--timestamps', nargs='*', help='timestamp set(s). see documentation for formatting guide')
argParser.add_argument('-ot', '--output-title', default='output', help='name of outputted video file or zip archive')
argParser.add_argument('-p', '--padding', default=5, type=int, choices=range(0, 31), metavar='[0-30]', help='see documentation')
argParser.add_argument('-dm', '--download-method', default='DPAMRE', type=str, choices=['DPAMRE', 'DWACFF'], metavar='[DPAMRE, DWACFF]', help='see documentation')
out_type = argParser.add_mutually_exclusive_group()
out_type.add_argument('-mr', '--output-merged', action='store_true', help='outputs clips as one merged video file')
out_type.add_argument('-ar', '--output-archive', action='store_true', help='outputs clips as seperate files to a zip archive')
argParser.add_argument('-cf', '--cookiefile', default=None, help='Netscape cookie file for downloading private and members only videos')
argParser.add_argument('--debug', action='store_true', help='print more detailed runtime information for debugging')
argParser.add_argument('-gui', '--use-gui', action='store_true', help='runs the program as a GUI window')
args = argParser.parse_args()
arg_list = args._get_args()

def run_cli():
	if args.video_links != None and args.timestamps != None:
		if args.debug:
			print(f"[DEBUG]: Inputted Video Link(s): {args.video_links}")
			print(f"[DEBUG]: Inputted Timestamp Set(s): {args.timestamps}")
					
		urlLinks = []
		timestampSets = []

		if len(args.video_links) > 1 or len(args.timestamps) > 1:
			print('[ERROR]: Multi-link functionality not yet implemented')
			sys.exit()
					
		for link in args.video_links:
			urlLinks.append(getAVUrls(args.debug, link, args.cookiefile))
					
		for set in args.timestamps:
			timestampSets.append(parseTimestamps(args.debug, set, args.padding))

		clip_dict = downloadClips(args.debug, timestampSets, urlLinks, ffmpeg_path, tempdir_parent_path, args.download_method)

		if clip_dict > 1:
			if args.output_merged:
				mergeClips(args.debug, clip_dict, args.output_title, ffmpeg_path, tempdir_parent_path)
			elif args.output_archive:
				compat_convert(tempdir_parent_path, ffmpeg_path)
				packupClips(args.output_title)
			else:
				for f in os.listdir(f"{tempdir_parent_path}/vcdl_temp"):
					if f.startswith('clip'):
						os.rename(os.path.join(f"{tempdir_parent_path}/vcdl_temp", f), os.path.join('./', f"{args.output_title}-{f}"))
		else:
			if os.path.exists(f"./{args.output_title}.mp4"):
				os.remove(f"./{args.output_title}.mp4")
			output_convert(args.output_title, tempdir_parent_path, ffmpeg_path)
		cleanup()
	else:
		argParser.print_help()

def run_gui(arguments = None):
	app = QApplication(sys.argv)
	x = MainWindow()
	app.exec()

def main():
	if sys.argv[1:]:
		if args.use_gui:
			run_gui(args)
			sys.exit(0)
		else:
			if args.debug:
				print(versionInfo())
				print(buildInfo())

			try:
				run_cli()
			except KeyboardInterrupt:
				print("\033[K", end="\r")
				print("[INFO]: Keyboard Interrupt recieved, exiting program...")
				cleanup()
			sys.exit(0)
	else:
		run_gui()
		sys.exit(0)

if __name__ == '__main__':
	main()
