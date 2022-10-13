# VCDL2
A Python rewrite of the original VCDL/HoloClipper PowerShell script.

VCDL2 retains much of the functionality of the original script. As with the original, it was purpose-written to specifications outlined by the HoloResort Translations team, however the program is open for all to use.

## Installation
Download the executable file from Releases, and place it wherever you like. It's advised to add it to your system PATH if possible. You can also build the program yourself using the `build.py` script. The `master` branch code should always be safe to build. Building on Windows has been tested and verified working. Building on Linux is supported, but only tested using a WSL2 shell as of writing (NOTE: you will have to build ffmpeg yourself on Linux). MacOS support will be added in a future update.

# Documentation

## Timestamp Formatting
Timestamps must be passed as a single string, with each entry seperated with a comma and no spaces. A timestamp "entry" is formatted as follows:
### **[x:yy:zz-x:yy:zz]**
- x: Hours
- yy: Minutes
- zz: Seconds

Hours can be omitted if not needed. Minutes will always need at least one digit, even if it is zero. Seconds always needs two digits, even if they are both zero. So, the smallest possible timestamp entry is `[0:00-0:00]`, which is zero minutes and zero seconds to zero minutes and zero seconds, however you won't get any video if you attempted to input it.

Some example timestamp entries are:
- `"[12:30-16:38],[38:40-42:01],[1:01:23-1:02:13]"`
- `"[0:13-1:18],[2:33-6:06]"`
- `"[28:59-30:00]"`

There is no limit to the number of timestamp entries you can pass at once. The only limit is your patience in waiting for every clip to download.

## Padding
Padding is exactly what it sounds like, extra video padded to the start and end of each clip. The padding value specifies how many extra seconds of video to add to the start and end of a clip.

## Download Methods
These are still under deveopment. The only two options avaliable right now are DPAMRE, and DWACFF.
| Method | Long Name | Description |
|:-------|:-----------------------------------------|:----------------------------------------------|
| DPAMRE | Download Portion and Minimize Re-Encodes | Attempts to download the requested clips only, while keeping re-encodes to a minimum.<br>**Best quality/performance balance, this setting is what most people will want to use.** |
| DWACFF | Download Whole and Cut From File | Downloads the entire video, then cuts clips locally from the downloaded file.<br>**Most useful for those with very fast internet connections, but less powerful PCs.**<br>**Also useful when cutting a large number of clips (10+) from the same video.**|

# New Features TODO:

## High Priority

- Multi-Link Video Stitching
- QT-Based GUI
- More detailed error reporting

## Medium Priority

- Integrated batch downloading
- Wider video site support

## Low Priority

- Improvements to downloading process efficiency
