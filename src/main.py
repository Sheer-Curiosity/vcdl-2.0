from clipper.utils import *

import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument('-v', '--video-links', nargs='*', required=True)
argParser.add_argument('-ts', '--timestamps', nargs=1)
args = argParser.parse_args()

urlLinks = []

for i in args.video_links:
	urlLinks.append(getAVUrls(i))

parseTimestamps("[0:00-1:00],[1:20-1:30],[1:30-1:55]", len(urlLinks))
