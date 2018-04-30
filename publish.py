#!/usr/bin/python

import sys
import os
import datetime

now = datetime.datetime.now()
pull_cmd = 'git pull'
add_cmd = 'git add .'
commit_cmd = 'git commit -a -m "published %s-%s-%s %s:%s"' % (now.year, now.month, now.day, now.hour, now.min)
push_cmd = 'git push'

os.chdir(sys.argv[1])
os.system(pull_cmd)
os.system(add_cmd)
os.system(commit_cmd)
os.system(push_cmd)