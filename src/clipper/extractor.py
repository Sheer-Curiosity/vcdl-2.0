from yt_dlp import *

class MyLogger:
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

def getAVUrls(videoLink: str):
	info = dict
	try:
		info = YoutubeDL({'quiet': True, 'no_warnings': True, 'logger': MyLogger(),}).extract_info(videoLink, download=False)
	except:
		exit()

	print(f"[EXTRACTOR]: Identified link as {info['extractor']}")

	if info['extractor'] == 'youtube':
		
		formats = info['formats'][::-1]
		best_video = next(f for f in formats if f['vcodec'] != 'none' and f['acodec'] == 'none' and f['ext'] == 'mp4')
		best_audio = next(f for f in formats if f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == 'm4a')

		return[best_video['url'], best_audio['url']]
	elif info['extractor'] == 'BiliBili':
		if 'entries' in info.keys():
			return [info['entries'][0]['url']]
		else:
			return [info['url']]
	else:
		print(f"[EXTRACTOR]: Extracting from {info['extractor']} not yet supported")