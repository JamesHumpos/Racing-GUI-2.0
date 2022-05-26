#! /usr/bin/python


import subprocess
import sys as sysname

## previously automatically updated script though Pi would kill original process when run on boot rather than from the main script. 
## now restarts the pi, at which point the auto run script also updates the script on every restart

subprocess.Popen(['sudo','shutdown','-r','now'])

## probably superfluous will check when able to test run on machine
sysname.exit(0)
