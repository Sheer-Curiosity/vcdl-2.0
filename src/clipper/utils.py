#This file will just chill here for the time being
from yt_dlp import *

def getAVUrls(videoLink):
	info = YoutubeDL({'quiet': True}).extract_info(videoLink, download=False)

	print(info['extractor'])

	if info['extractor'] == 'youtube':
	
		formats = info['formats'][::-1]
		best_video = next(f for f in formats if f['vcodec'] != 'none' and f['acodec'] == 'none' and f['ext'] == 'mp4')
		best_audio = next(f for f in formats if f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == 'm4a')

		print(best_video['resolution'])
		return[best_video['url'], best_audio['url']]
	
	if info['extractor'] == 'BiliBili':
		if 'entries' in info.keys():
			return [info['entries'][0]['url']]
		else:
			return [info['url']]

def formatTimestampPair(inputString):
	print()
