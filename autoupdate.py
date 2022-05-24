#! /usr/bin/python

import git 
import time as pause
pause.sleep(5)

repo = git.Repo('/home/james/GUIGIT')
repo.remotes.origin.pull('master')


