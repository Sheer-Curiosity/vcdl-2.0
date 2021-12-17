import ffmpeg
import os

def mergeClips(numClips: int, outputName: str):
	tempdirFiles = [f for f in os.listdir('./vcdl_temp') if os.path.isfile(os.path.join('./vcdl_temp', f))]
	videoFiles = []
	concatIn = []
	idx = int(0)

	for file in tempdirFiles:
		if (idx) < numClips:
			if file.startswith('clip'):
				videoFiles.append(ffmpeg.input(f"./vcdl_temp/{file}"))
				idx += 1
			else:
				continue
	
	for vid in videoFiles:
		concatIn.append(vid.video)
		concatIn.append(vid.audio)
	
	print(f"[MERGER]: Merging {len(concatIn)} streams from {len(videoFiles)} video files...")
	process = (
	ffmpeg
		.concat(*concatIn, v=1, a=1)
		.output(f"./{outputName}.mp4")
		.global_args('-hide_banner', '-loglevel', 'quiet', '-stats', '-y', '-crf', '18')
		.run_async(quiet=True)
	)
	outbuff = bytearray()
	while True:
		output = process.stderr.read(1)
		if output == b'' and process.poll() is not None:
			break
		if output == b'\r':
			outbuff += output
			print(outbuff.decode('utf-8'), end='')
			outbuff = bytearray()
		else:
			outbuff += output
	print(outbuff.decode('utf-8'), end='')
	