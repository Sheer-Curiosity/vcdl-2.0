from clipper.utils import *

import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument('-v', '--video-links', nargs='*', required=True)
# argParser.add_argument('-ts', '--timestamps', required=True)
args = argParser.parse_args()

thing = getAVUrls(args.video_links[0])

print(thing[0])
