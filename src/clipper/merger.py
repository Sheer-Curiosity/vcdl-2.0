import ffmpeg
import os

def mergeClips(debug: bool, maximizeCompat: bool, numClips: int, outputName: str, ffmpeg_path: str, tempdir_parent_path: str):
	tempdirFiles = []
	videoFiles = []
	concatIn = []
	idx = 0

	for entry in os.listdir(f"{tempdir_parent_path}/vcdl_temp"):
		if os.path.isfile(os.path.join(f"{tempdir_parent_path}/vcdl_temp", entry)):
			tempdirFiles.append(entry)

	with open(f"{tempdir_parent_path}/vcdl_temp/clips.txt", 'w') as lst:
		for file in tempdirFiles:
			if (idx) < numClips:
				if file.startswith('clip'):
					filePath = f"{tempdir_parent_path}/vcdl_temp/{file}"
					lst.write(f"file '{os.path.abspath(filePath)}'")
					lst.write('\n')
					videoFiles.append(ffmpeg.input(f"{tempdir_parent_path}/vcdl_temp/{file}"))
					idx += 1
				else:
					continue
	
	for vid in videoFiles:
		concatIn.append(vid.video)
		concatIn.append(vid.audio)
	
	print(f"[MERGER]: Merging {len(concatIn)} streams from {len(videoFiles)} video files...")
	if debug:
		if (maximizeCompat):
			print(f"[MERGER/DEBUG]: Maximize Compatibility enabled")
		else:
			print(f"[MERGER/DEBUG]: Maximize Compatibility disabled")
		
	
	if (maximizeCompat):
		process = (
		ffmpeg
			.concat(*concatIn, v=1, a=1)
			.output(f"./{outputName}.mp4", vcodec='libx264')
			.global_args('-hide_banner', '-loglevel', 'quiet', '-stats', '-y', '-crf', '18')
			.run_async(cmd=ffmpeg_path, quiet=True)
		)
	else:
		process = (
		ffmpeg
			.input(f"{tempdir_parent_path}/vcdl_temp/clips.txt", **{'f': 'concat', 'safe': 0})
			.output(f"./output.mp4", vcodec='copy', acodec='copy')
			.global_args('-hide_banner', '-loglevel', 'quiet', '-stats', '-y')
			.run_async(cmd=ffmpeg_path, quiet=True)
		)
	outbuff = bytearray()
	while True:
		output = process.stderr.read(1)
		if output == b'' and process.poll() is not None:
			break
		if output == b'\r':
			outbuff += output
			print(f"[FFMPEG]: {outbuff.decode('utf-8')}", end='')
			outbuff = bytearray()
		else:
			outbuff += output
	print(f"[FFMPEG]: {outbuff.decode('utf-8')}", end='')
	