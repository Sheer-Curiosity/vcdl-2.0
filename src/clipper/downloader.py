import ffmpeg
import os

def downloadClips(startTimestamps: list, runtimeTimestamps: list, links: list):
	if len(links) > 1:
		print('Funtionality Not Yet Implemented')
	else:
		if not os.path.isdir('./vcdl_temp'):
			os.mkdir('./vcdl_temp')
		if len(links[0]) > 1:
			print('YouTube')
			print(startTimestamps)
			for idx, stmp in enumerate(startTimestamps):
				videoInput = ffmpeg.input(links[0][0], ss=stmp, t=runtimeTimestamps[idx])
				audioInput = ffmpeg.input(links[0][1], ss=stmp, t=runtimeTimestamps[idx])
				vcodec = 'libx264'
				if stmp == '00:00:00.00':
					vcodec = 'copy'
				test = (
					ffmpeg
					.output(videoInput, audioInput, f"./vcdl_temp/clip{idx}.mp4", vcodec=vcodec, acodec='copy')
					.global_args('-hide_banner', '-loglevel', 'quiet', '-stats', '-y')
					.run(quiet=True)
				)
				print(test)
		else:
			print('BiliBili')
		
