import ffmpeg
import os
import sys
import zipfile

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
def parseTimestamps(debug: bool, timestampsInput: str, timePadding: int):
	initSplitList = timestampsInput.split(',')
	tsList = []
	paddedTs = []
	for i in initSplitList:
		tsList.append(i.strip('[]'))
	for ts in tsList:
		for out in calculatePadding(ts, timePadding):
			paddedTs.append(out)
	for idx, val in enumerate(paddedTs):
		if idx < (len(paddedTs)-1) and idx % 2 != 0:
			if paddedTs[idx+1][0] <= paddedTs[idx][0]:
				if paddedTs[idx+1][1] <= paddedTs[idx][1]:
					if paddedTs[idx+1][2] <= paddedTs[idx][2]:
						if paddedTs[idx+1][3] <= paddedTs[idx][3]:
							paddedTs[idx+1] = 'OVERLAP'
							paddedTs[idx] = 'OVERLAP'
							print(f"[TIMESTAMPS]: Post-buffer duration overlap found, combining clips {idx-1} and {idx}")
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
	
	return [startStamps, runtimeStamps]

def cleanup():
	tempdirFiles = [f for f in os.listdir('./vcdl_temp') if os.path.isfile(os.path.join('./vcdl_temp', f))]

	print('[CLEANUP]: Clearing temp directory...')
	for file in tempdirFiles:
		print(f"[CLEANUP]: Removing file - {file}\r", end='')
		os.remove(f"./vcdl_temp/{file}")
	print()
	os.rmdir('./vcdl_temp')

def packupClips(output_title: str):
	print('[CLEANUP]: Packing clips into zip archive...')
	with zipfile.ZipFile(f"./{output_title}.zip", 'w') as zipObj:
		for f in os.listdir('./vcdl_temp'):
			if f.startswith('clip'):
				zipObj.write(os.path.join('./vcdl_temp', f), os.path.join('.', f))

def output_convert(output_title: str, tempdir_parent_path: str, ffmpeg_path: str):
	print('[CLEANUP]: Converting output file...')
	clip = ffmpeg.input(f"{tempdir_parent_path}/vcdl_temp/clip1.mp4")
	convProc = (
		ffmpeg
		.output(clip, f"./{output_title}.mp4", vcodec='libx264', acodec='copy')
		.global_args('-hide_banner', '-loglevel', 'quiet', '-stats', '-y', '-crf', '16')
		.run_async(cmd=ffmpeg_path, quiet=True)
	)
	outbuff = bytearray()
	while True:
		convProcOutput = convProc.stderr.read(1)
		if convProcOutput == b'' and convProc.poll() is not None:
			break
		if convProcOutput == b'\r':
			outbuff += convProcOutput
			print(f"[FFMPEG]: {outbuff.decode('utf-8')}", end='')
			outbuff = bytearray()
		else:
			outbuff += convProcOutput
	print(f"[FFMPEG]: {outbuff.decode('utf-8')}", end='')

def compat_convert(tempdir_parent_path: str, ffmpeg_path: str):
	for idx, f in enumerate(os.listdir(f"{tempdir_parent_path}/vcdl_temp")):
		if f.startswith('clip'):
			print(f"[CLEANUP]: Converting clip {idx+1}...")
			src = open(os.path.join(f"{tempdir_parent_path}/vcdl_temp", f), 'rb').read()
			open(os.path.join(f"{tempdir_parent_path}/vcdl_temp", f"TEMP_{f}"), 'wb').write(src)
			clip = ffmpeg.input(os.path.join(f"{tempdir_parent_path}/vcdl_temp", f"TEMP_{f}"))
			convProc = (
				ffmpeg
				.output(clip, os.path.join(f"{tempdir_parent_path}/vcdl_temp", f), vcodec='libx264', acodec='copy')
				.global_args('-hide_banner', '-loglevel', 'quiet', '-stats', '-y', '-crf', '16')
				.run_async(cmd=ffmpeg_path, quiet=True)
			)
			outbuff = bytearray()
			while True:
				convProcOutput = convProc.stderr.read(1)
				if convProcOutput == b'' and convProc.poll() is not None:
					break
				if convProcOutput == b'\r':
					outbuff += convProcOutput
					print(f"[FFMPEG]: {outbuff.decode('utf-8')}", end='')
					outbuff = bytearray()
				else:
					outbuff += convProcOutput
			print(f"[FFMPEG]: {outbuff.decode('utf-8')}", end='')
			os.remove(os.path.join(f"{tempdir_parent_path}/vcdl_temp", f"TEMP_{f}"))

