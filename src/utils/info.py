import git

__version = 'DEV-0.2.3'

def versionInfo(isDev: bool):
	if isDev:
		repo = git.Repo(search_parent_directories=True)
		sha = repo.head.object.hexsha
		return (f"[DEBUG]: Current Major Version: {__version}\n[DEBUG]: Git Commit SHA: {sha}\n")
	else:
		return (f"[DEBUG]: Current Major Version: {__version}\n")

def generalInfo():
	return(
	'''Written By: Sheer Curiosity
Tested By: Sheer Curiosity, Chimatta
Quote Of The Version:
  "I wrote most of this program in
  24 hours over the span of 2 days,
  powered by nothing but eurobeat
  and determination."
  - Sheer Curiosity\n
	''')