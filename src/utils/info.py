import os

def versionInfo():
	return (f"[DEBUG]: Current Version: {read_version()}\n")

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

def read_version():
    exec(compile(open('src/version.py').read(), 'src/version.py', 'exec'))
    return locals()['__version__']
