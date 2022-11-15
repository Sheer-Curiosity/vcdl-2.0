from yt_dlp import *
import re
import sys

class BasicLogger:
	def debug(self, msg):
		if msg.startswith('[debug] '):
			pass
		else:
			self.info(msg)

	def info(self, msg):
		pass

	def warning(self, msg):
		pass

	def error(self, msg):
		print(f"[EXTRACTOR]: {msg}")

def getAVUrls(debug: bool, videoLink: str, useAv1: bool, cookieFile: str):
	info = dict
	try:
		info = YoutubeDL({'quiet': True, 'no_warnings': True, 'logger': BasicLogger(), 'cookiefile': cookieFile}).extract_info(videoLink, download=False)
	except:
		sys.exit()

	print(f"[EXTRACTOR]: Identified link as {info['extractor']}")

	if info['extractor'] == 'youtube':
		
		formats = info['formats'][::-1]
		if (useAv1):
			try:
				codec = "av01"
				best_video = next(f for f in formats if f['vcodec'].startswith(codec) and f['ext'] == 'mp4')
			except:
				codec = "avc1"
				best_video = next(f for f in formats if f['vcodec'].startswith(codec) and f['ext'] == 'mp4')
			best_audio = next(f for f in formats if f['acodec'].startswith('mp4a') and f['ext'] == 'm4a')
		else:
			codec = "avc1"
			best_video = next(f for f in formats if f['vcodec'].startswith(codec) and f['ext'] == 'mp4')
			best_audio = next(f for f in formats if f['acodec'].startswith('mp4a') and f['ext'] == 'm4a')

		if debug:
			print(f"[EXTRACTOR/DEBUG]: VCodec: {best_video['vcodec']}")
			print(f"[EXTRACTOR/DEBUG]: ACodec: {best_audio['acodec']}")
			print(f"[EXTRACTOR/DEBUG]: Resolution: {best_video['resolution']}")

		return[best_video['url'], best_audio['url'], codec]
	elif info['extractor'] == 'BiliBili':
		if 'entries' in info.keys():
			return [info['entries'][0]['url']]
		else:
			return [info['url']]
	else:
		print(f"[EXTRACTOR]: Extracting from {info['extractor']} not yet supported")