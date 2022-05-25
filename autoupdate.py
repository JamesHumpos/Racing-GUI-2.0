#! /usr/bin/python

import git 
import time as pause
import subprocess
import sys as sysname
pause.sleep(5)

repo = git.Repo('/home/james/GUIGIT')
repo.git.reset('--hard')
repo.remotes.origin.pull('master')

pause.sleep(15)
subprocess.Popen(['python', "/home/james/GUIGIT/FullGUI.py"])
sysname.exit(0)
