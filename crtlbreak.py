#!/usr/local/bin/python
#-*- coding: utf-8 -*-
import re,sys
import string
import signal

def sigint_handler(signum, frame):
    global is_sigint_up
    is_sigint_up = True
    print ('catched interrupt signal!')

signal.signal(signal.SIGINT, sigint_handler)
signal.signal(signal.SIGHUP, sigint_handler)
signal.signal(signal.SIGTERM, sigint_handler)
is_sigint_up = False
while True:
    try:
        # 你想做的事情
        import time
        print ("start .............")
        time.sleep(2)
        if is_sigint_up:
            # 中断时需要处理的代码
            print ("Exit")
            is_sigint_up = False
            exit(1)
            #continue
    except:
    #    Excepting,e
        break
