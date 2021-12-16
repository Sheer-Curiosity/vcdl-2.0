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

def formatTimestamp(inputTimestamp: list):
	tempTimestamp = inputTimestamp
	for idx, entry in enumerate(inputTimestamp):
		if len(str(entry)) < 2:
			tempTimestamp[idx] = f"0{str(entry)}"
	return f"{tempTimestamp[0]}:{tempTimestamp[1]}:{tempTimestamp[2]}.{tempTimestamp[3]}"

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
	startTs.append(0)
	endTs.append(0)

	return[startTs, endTs]

# There is 100% a better way to do some of the logic in this function, but I really really do not care.
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
			for out in calculatePadding(ts, 5):
				paddedTs.append(out)
		for idx, val in enumerate(paddedTs):
			if idx < (len(paddedTs)-1) and idx % 2 != 0:
				if paddedTs[idx+1][0] <= paddedTs[idx][0]:
					if paddedTs[idx+1][1] <= paddedTs[idx][1]:
						if paddedTs[idx+1][2] <= paddedTs[idx][2]:
							if paddedTs[idx+1][3] <= paddedTs[idx][3]:
								paddedTs[idx+1] = 'OVERLAP'
								paddedTs[idx] = 'OVERLAP'
		while 'OVERLAP' in paddedTs:
			paddedTs.remove('OVERLAP')
		startStamps = []
		endStamps = []
		runtimeStamps = []
		for idx2, val2 in enumerate(paddedTs):
			if idx2 % 2 != 0:
				endStamps.append(val2)
			else:
				startStamps.append(val2)
		for idx3, val3 in enumerate(startStamps):
			rtList = []
			for x in range(0, 4):
				rtList.append(endStamps[idx3][x] - val3[x])
			if rtList[2] < 0:
				rtList[2] += 60
				rtList[1] -= 1
			if rtList[1] < 0:
				rtList[1] += 60
				rtList[0] += 1
			runtimeStamps.append(rtList)
		for idx4, stmp in enumerate(startStamps):
			startStamps[idx4] = formatTimestamp(stmp)
			runtimeStamps[idx4] = formatTimestamp(runtimeStamps[idx4])
		
		return startStamps, runtimeStamps