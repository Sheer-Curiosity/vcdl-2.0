from yt_dlp import *

def getAVUrls(videoLink: str):
	info = YoutubeDL({'quiet': True, 'no_warnings': True}).extract_info(videoLink, download=False)

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

def formatTimestamp(inputTimestamp: str):
	print()

def calculatePadding(timestampPair: str, paddingInt: int):
	stamps = timestampPair.split('-')
	startTs = []
	endTs = []
	for st in stamps[0].split(':'):
		startTs.append(int(st))
	for st in stamps[1].split(':'):
		endTs.append(int(st))
	
	if len(startTs) == 2:
		startTs.insert(0, 0)
		while startTs[1] >= 60:
			startTs[1] -= 60
			startTs[0] += 1
	if len(endTs) == 2:
		endTs.insert(0, 0)
		while endTs[1] >= 60:
			endTs[1] -= 60
			endTs[0] += 1
	if startTs[2] < paddingInt and startTs[1] == 0 and startTs[0] == 0:
		startTs[2] = 0
	else:
		startTs[2] -= paddingInt
	endTs[2] += paddingInt
	if startTs[2] < 0:
		startTs[2] += 60
		startTs[1] -= 1
	if startTs[1] < 0:
		startTs[1] += 60
		startTs[0] -= 1
	if endTs[2] >= 60:
			endTs[2] -= 60
			endTs[1] += 1
	if endTs[1] >= 60:
			endTs[1] -= 60
			endTs[0] += 1

	return[startTs, endTs]


def parseTimestamps(timestampsInput: str, numVideoLinks: int):
	initSplitList = timestampsInput.split(',')

	idList = []
	tsList = []
	if numVideoLinks > 1:
		for i in initSplitList:
			splitIdAndTs = i.split(':', 1)
			idList.append(splitIdAndTs[0])
			tsList.append(splitIdAndTs[1].strip('[]'))
		if int(max(idList)) != numVideoLinks-1:
			print(f"ERROR: Timestamp ID {max(idList)} out of range")
			quit()
	else:
		paddedTs = []
		for i in initSplitList:
			tsList.append(i.strip('[]'))
		for ts in tsList:
			paddedTs.append(calculatePadding(ts, 5))
		print(paddedTs)
	


