#!/usr/bin/python
# -*- coding: utf-8 -*-

import psutil
import re, os

if __name__ == '__main__':
    pids = psutil.pids()
    for pid in pids:
        if re.search('uwsgi', psutil.Process(pid).name()):
            kill = 'kill -HUP ' + str(pid)
            os.system(kill)
            print kill
