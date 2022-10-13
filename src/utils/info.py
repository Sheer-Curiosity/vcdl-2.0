import os
from version import __version__

def buildInfo():
	return (f"[DEBUG]: Build: {__version__.split('.')[3]}")

def versionInfo():
  return (f"[DEBUG]: Version: {'.'.join(__version__.split('.')[:3])}")

def generalInfo():
	return(
	'''Written By: Sheer Curiosity
Tested By: Sheer Curiosity, Members of HoloRes Translations
Quote Of The Version:
  "I wrote most of this program in
  24 hours over the span of 3 days,
  powered by nothing but eurobeat
  and determination."
  - Sheer Curiosity\n
	''')
