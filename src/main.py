# I did not use pyton to code this by choice. I absolutely hate python. It doesn't make sense to me when I read it, and in my opinion
# using indents as syntax is the most idiotic thing ever. But, it was the most suitable language to solve the problem I have, and thus
# my hand is forced.
#
# Reluctantly programmed and tested by Sheer Curiosity

from clipper.utils import *
from clipper.downloader import *

import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument('-v', '--video-links', nargs='*')
argParser.add_argument('-ts', '--timestamps')
args = argParser.parse_args()

print(args.timestamps)

def runClipper(video_links: list, timestamps: str):
	urlLinks = []

	for i in video_links:
		urlLinks.append(getAVUrls(i))
	
	startTs, runtimeTs = parseTimestamps(timestamps, len(urlLinks))
	downloadClips(startTs, runtimeTs, urlLinks)

runClipper(args.video_links, args.timestamps)
