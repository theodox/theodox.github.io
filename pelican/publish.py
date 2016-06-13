#!/usr/bin/env python

import sys
import os
import datetime

now = datetime.datetime.now()
commit_cmd = 'git commit -a -m "published %s-%s-%s %s:%s"' % (now.year, now.month, now.day, now.hour, now.min)
push_cmd = 'git push'

os.chdir(sys.argv[1])
os.system(commit_cmd)
os.system(push_cmd)