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
import sys

ffmpeg_path = resource_path('bin/ffmpeg/ffmpeg', os.path.abspath(__file__))

argParser = argparse.ArgumentParser()
argParser.add_argument('-v', '--video-links', nargs='*')
argParser.add_argument('-ts', '--timestamps')
argParser.add_argument('-o', '--output-title', default='output')
argParser.add_argument('-p', '--padding', default=5, type=int, choices=range(0, 31), metavar='[0-30]')
argParser.add_argument('-ext', '--output-file-extension', default='mp4', type=str, choices=['mp4', 'mkv'], metavar='[mp4, mkv]')
argParser.add_argument('-m', '--merge', action='store_true', help='merge clips into one video file')
argParser.add_argument('--debug', action='store_true', help='print more detailed information for debugging')
argParser.add_argument('--cookiefile', default=None)
args = argParser.parse_args()

def runClipper(video_links: list, timestamps: str):
	urlLinks = []

	if len(video_links) > 1:
		print('[EXTRACTOR]: Multi-link functionality not yet implemented')
		sys.exit()
	for i in video_links:
		urlLinks.append(getAVUrls(i, args.cookiefile))
	
	startTs, runtimeTs = parseTimestamps(timestamps, len(urlLinks), args.padding )

	numClips = downloadClips(startTs, runtimeTs, urlLinks, ffmpeg_path)
	if numClips > 1:
		if args.merge:
			mergeClips(numClips, args.output_title, ffmpeg_path)
		else:
			packupClips(args.output_title)
	else:
		if os.path.exists(f"./{args.output_title}.mp4"):
			os.remove(f"./{args.output_title}.mp4")
		os.rename('./vcdl_temp/clip1.mp4', f"./{args.output_title}.mp4")
	cleanup()

if args.debug:
	print(versionInfo(), end="")

if args.video_links != None and args.timestamps != None:
	if args.debug:
		print(f"[DEBUG]: Inputted Video Link(s): {args.video_links}")
		print(f"[DEBUG]: Inputted Timestamps: {args.timestamps}")
	runClipper(args.video_links, args.timestamps)
