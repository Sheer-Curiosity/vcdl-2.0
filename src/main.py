# I did not use pyton to code this by choice. I absolutely hate python. It doesn't make sense to me when I read it, and in my opinion
# using indents as syntax is the most idiotic thing ever. But, it was the most suitable language to solve the problem I have, and thus
# my hand is forced.
#
# Reluctantly written by Sheer Curiosity

from clipper.utils import *
from clipper.downloader import *
from utils.info import *

import argparse
import os

isDev = False
if os.path.isdir('./.git'):
	isDev = True

argParser = argparse.ArgumentParser()
argParser.add_argument('-v', '--video-links', nargs='*')
argParser.add_argument('-ts', '--timestamps')
argParser.add_argument('--debug', action='store_true')
args = argParser.parse_args()

def runClipper(video_links: list, timestamps: str):
	urlLinks = []

	if len(video_links) > 1:
		print('[EXTRACTOR]: Multi-link functionality not yet implemented')
		exit()
	for i in video_links:
		urlLinks.append(getAVUrls(i))
	
	startTs, runtimeTs = parseTimestamps(timestamps, len(urlLinks))
	numClips = downloadClips(startTs, runtimeTs, urlLinks)
	print(numClips)

if args.debug:
	print(versionInfo(isDev), end="")

if args.video_links != None and args.timestamps != None:
	if args.debug:
		print(f"[DEBUG]: Inputted Video Link(s): {args.video_links}")
		print(f"[DEBUG]: Inputted Timestamps: {args.timestamps}")
	runClipper(args.video_links, args.timestamps)
