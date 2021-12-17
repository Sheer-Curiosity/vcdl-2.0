import ffmpeg
import os
import subprocess

def downloadClips(startTimestamps: list, runtimeTimestamps: list, links: list):
	if len(links) > 1:
		print('[DOWNLOADER]: Funtionality not yet implemented')
		exit()
	else:
		if not os.path.isdir('./vcdl_temp'):
			os.mkdir('./vcdl_temp')
		if len(links[0]) > 1:
			print(f"[DOWNLOADER]: {len(startTimestamps)} clips found to download")
			for idx, stmp in enumerate(startTimestamps):
				print(f"[DOWNLOADER]: Downloading clip {idx+1}...")
				videoInput = ffmpeg.input(links[0][0], ss=stmp, t=runtimeTimestamps[idx])
				audioInput = ffmpeg.input(links[0][1], ss=stmp, t=runtimeTimestamps[idx])
				vcodec = 'libx264'
				if stmp == '00:00:00.00':
					vcodec = 'copy'
				downloadProc = (
					ffmpeg
					.output(videoInput, audioInput, f"./vcdl_temp/clip{idx+1}.mp4", vcodec=vcodec, acodec='copy')
					.global_args('-hide_banner', '-loglevel', 'quiet', '-stats', '-y')
					.run_async(quiet=True)
				)
				outbuff = bytearray()
				while True:
					dlProcOutput = downloadProc.stderr.read(1)
					if dlProcOutput == b'' and downloadProc.poll() is not None:
						break
					if dlProcOutput == b'\r':
						outbuff += dlProcOutput
						print(outbuff.decode('utf-8'), end='')
						outbuff = bytearray()
					else:
						outbuff += dlProcOutput
				print(outbuff.decode('utf-8'))
			return (len(startTimestamps))
		else:
			print('[DOWNLOADER]: BiliBili downloading not yet implemented')
			exit()
		
