from yt_dlp import *
import ffmpeg
import os

# The 'method' parameter is meant for future use.
# a few I have planned so far, labeled in terms of priority to add:
# - (2) DPAREA: Download Portion and Re-Encode All (older brother to DPAMRE, yields lower quality at a lower speed, but standardizes all downloaded files)
# - (0) DPAMRE: Download Portion and Minimize Re-Encode (current hardcoded method, best quality/speed ratio, lacks uniformity in downloaded files)
# - (1) DWACFF: Download Whole and Cut From File (Useful if you have a slow PC but fast internet, fewer re-encodes)
# - (3) DWACFI: Download Whole and Create From Images (REALLY FUCKING SLOW, came to me in a dream (I wish I was joking))
# It's like the whole "multiple solutions to one problem" thing, except some
# solutions are better for some permutations of the problem than others. So
# rather than deciding for the user which answer is best, I'll let them
# choose.

DPAMRE = {
	'name': 'DPAMRE',
	'desc': "Download Portion and Minimize Re-Encode"
}
DWACFF = {
	'name': 'DWACFF',
	'desc': "Download Whole and Cut From File"
}

def downloadClips(debug: bool, timestamps: list, links: list, ffmpeg_path: str, tempdir_parent_path: str, method: str):
	if len(links) > 1:
		# TODO
		print()
	else:
		startTimestamps = timestamps[0][0]
		runtimeTimestamps = timestamps[0][1]
		
		if not os.path.isdir(f"{tempdir_parent_path}/vcdl_temp"):
			os.mkdir(f"{tempdir_parent_path}/vcdl_temp")
		if method.upper() == DPAMRE['name']:
			if debug:
				print(f"[DOWNLOADER/DEBUG]: Using {DPAMRE['name']} ({DPAMRE['desc']}) download method")
			if len(links[0]) > 1:
				print(f"[DOWNLOADER]: {len(startTimestamps)} clip(s) found to download")
				for idx, stmp in enumerate(startTimestamps):
					print(f"[DOWNLOADER]: Downloading clip {idx+1}...")
					videoInput = ffmpeg.input(links[0][0], ss=stmp, t=runtimeTimestamps[idx])
					audioInput = ffmpeg.input(links[0][1], ss=stmp, t=runtimeTimestamps[idx])
					if links[0][2] == 'av01':
						vcodec = 'libsvtav1'
					else:
						vcodec = 'libx264'
					if stmp == '00:00:00.00':
						vcodec = 'copy'
						downloadProc = (
							ffmpeg
							.output(videoInput, audioInput, f"{tempdir_parent_path}/vcdl_temp/clip{idx+1}.mp4", vcodec=vcodec, acodec='copy')
							.global_args('-hide_banner', '-loglevel', 'quiet', '-stats', '-y')
							.run_async(cmd=ffmpeg_path, quiet=True)
						)
					else:
						downloadProc = (
							ffmpeg
							.output(videoInput, audioInput, f"{tempdir_parent_path}/vcdl_temp/clip{idx+1}.mp4", vcodec=vcodec, acodec='copy')
							.global_args('-hide_banner', '-loglevel', 'fatal', '-stats', '-y', '-crf', '18')
							.run_async(cmd=ffmpeg_path, quiet=True)
						)
					if (debug):
						print(f"[DOWNLOADER/DEBUG]: Using vcodec {vcodec}")
					outbuff = bytearray()
					while True:
						dlProcOutput = downloadProc.stderr.read(1)
						if dlProcOutput == b'' and downloadProc.poll() is not None:
							break
						if dlProcOutput == b'\r':
							outbuff += dlProcOutput
							print(f"[FFMPEG]: {outbuff.decode('utf-8')}", end='')
							outbuff = bytearray()
						else:
							outbuff += dlProcOutput
					print(f"[FFMPEG]: {outbuff.decode('utf-8')}", end='')
				return (len(startTimestamps))
			else:
				print(f"[DOWNLOADER]: {len(startTimestamps)} clip(s) found to download")
				for idx, stmp in enumerate(startTimestamps):
					print(f"[DOWNLOADER]: Downloading clip {idx+1}...")
					videoInput = ffmpeg.input(links[0][0], ss=stmp, t=runtimeTimestamps[idx])
					vcodec = 'copy'
					downloadProc = (
						ffmpeg
						.output(videoInput, f"{tempdir_parent_path}/vcdl_temp/clip{idx+1}.mp4", vcodec=vcodec, acodec='copy')
						.global_args('-hide_banner', '-loglevel', 'quiet', '-stats', '-y')
						.run_async(cmd=ffmpeg_path, quiet=True)
					)
					outbuff = bytearray()
					while True:
						dlProcOutput = downloadProc.stderr.read(1)
						if dlProcOutput == b'' and downloadProc.poll() is not None:
							break
						if dlProcOutput == b'\r':
							outbuff += dlProcOutput
							print(f"[FFMPEG]: {outbuff.decode('utf-8')}", end='')
							outbuff = bytearray()
						else:
							outbuff += dlProcOutput
					print(f"[FFMPEG]: {outbuff.decode('utf-8')}", end='')
				return (len(startTimestamps))
		if method == DWACFF['name']:
			if debug:
				print(f"[DOWNLOADER/DEBUG]: Using {DWACFF['name']} ({DWACFF['desc']}) download method")
			if len(links[0]) > 1:
				print(f"[DOWNLOADER]: {len(startTimestamps)} clip(s) found to download")
				print(f"[DOWNLOADER]: Downloading source video...")
				videoInput = ffmpeg.input(links[0][0])
				audioInput = ffmpeg.input(links[0][1])
				downloadProc = (
					ffmpeg
					.output(videoInput, audioInput, f"{tempdir_parent_path}/vcdl_temp/main.mp4", vcodec='copy', acodec='copy')
					.global_args('-hide_banner', '-loglevel', 'quiet', '-stats', '-y')
					.run_async(cmd=ffmpeg_path, quiet=True)
				)
				outbuff = bytearray()
				while True:
					dlProcOutput = downloadProc.stderr.read(1)
					if dlProcOutput == b'' and downloadProc.poll() is not None:
						break
					if dlProcOutput == b'\r':
						outbuff += dlProcOutput
						print(f"[FFMPEG]: {outbuff.decode('utf-8')}", end='')
						outbuff = bytearray()
					else:
						outbuff += dlProcOutput
				print(f"[FFMPEG]: {outbuff.decode('utf-8')}", end='')
				for idx, stmp in enumerate(startTimestamps):
					print(f"[DOWNLOADER]: Cutting clip {idx+1}...")
					mainInput = ffmpeg.input(f"{tempdir_parent_path}/vcdl_temp/main.mp4", ss=stmp, t=runtimeTimestamps[idx])
					downloadProc = (
						ffmpeg
						.output(mainInput, f"{tempdir_parent_path}/vcdl_temp/clip{idx+1}.mp4", vcodec='copy', acodec='copy')
						.global_args('-hide_banner', '-loglevel', 'quiet', '-stats', '-y')
						.run_async(cmd=ffmpeg_path, quiet=True)
					)
					outbuff = bytearray()
					while True:
						dlProcOutput = downloadProc.stderr.read(1)
						if dlProcOutput == b'' and downloadProc.poll() is not None:
							break
						if dlProcOutput == b'\r':
							outbuff += dlProcOutput
							print(f"[FFMPEG]: {outbuff.decode('utf-8')}", end='')
							outbuff = bytearray()
						else:
							outbuff += dlProcOutput
					print(f"[FFMPEG]: {outbuff.decode('utf-8')}", end='')
				return (len(startTimestamps))
			else:
				print(f"[DOWNLOADER]: {len(startTimestamps)} clip(s) found to download")
				print(f"[DOWNLOADER]: Downloading video...")
				videoInput = ffmpeg.input(links[0][0])
				downloadProc = (
					ffmpeg
					.output(videoInput, f"{tempdir_parent_path}/vcdl_temp/main.mp4", vcodec='copy', acodec='copy')
					.global_args('-hide_banner', '-loglevel', 'quiet', '-stats', '-y')
					.run_async(cmd=ffmpeg_path, quiet=True)
				)
				outbuff = bytearray()
				while True:
					dlProcOutput = downloadProc.stderr.read(1)
					if dlProcOutput == b'' and downloadProc.poll() is not None:
						break
					if dlProcOutput == b'\r':
						outbuff += dlProcOutput
						print(f"[FFMPEG]: {outbuff.decode('utf-8')}", end='')
						outbuff = bytearray()
					else:
						outbuff += dlProcOutput
				print(f"[FFMPEG]: {outbuff.decode('utf-8')}", end='')
				for idx, stmp in enumerate(startTimestamps):
					print(f"[DOWNLOADER]: Cutting clip {idx+1}...")
					mainInput = ffmpeg.input(f"{tempdir_parent_path}/vcdl_temp/main.mp4", ss=stmp, t=runtimeTimestamps[idx])
					downloadProc = (
						ffmpeg
						.output(mainInput, f"{tempdir_parent_path}/vcdl_temp/clip{idx+1}.mp4", vcodec='copy', acodec='copy')
						.global_args('-hide_banner', '-loglevel', 'quiet', '-stats', '-y')
						.run_async(cmd=ffmpeg_path, quiet=True)
					)
					outbuff = bytearray()
					while True:
						dlProcOutput = downloadProc.stderr.read(1)
						if dlProcOutput == b'' and downloadProc.poll() is not None:
							break
						if dlProcOutput == b'\r':
							outbuff += dlProcOutput
							print(f"[FFMPEG]: {outbuff.decode('utf-8')}", end='')
							outbuff = bytearray()
						else:
							outbuff += dlProcOutput
					print(f"[FFMPEG]: {outbuff.decode('utf-8')}", end='')
				return (len(startTimestamps))
