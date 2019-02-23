#!/usr/bin/env python3
# -*- coding:utf-8 -*-


__author__    = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018'

import colored
import datetime
import logging
import sys

logging.basicConfig(stream=sys.stdout, \
                    level=logging.DEBUG, \
                    format=colored.stylize('%(asctime)s - %(levelname)8s - %(message)s', colored.fore.DARK_GRAY))

def _log(level, colorcode, *objs):
    msg = ' '.join(map(str, objs)).replace('\n', '\n                                     ')
    logging.log(level, colored.stylize(msg, colorcode))

def print_title(*objs):
    _log(logging.CRITICAL, colored.fore.CYAN+colored.style.BOLD, *objs)
    pass

def print_subtitle(*objs):
    _log(logging.INFO, colored.fore.CYAN, *objs)
    pass

def print_info(*objs):
    _log(logging.INFO, colored.fore.MAGENTA+colored.style.BOLD, *objs)
    pass

def print_status(*objs):
    _log(logging.INFO, colored.fore.YELLOW, *objs)
    pass

def print_debug(*objs):
    _log(logging.DEBUG, colored.fore.YELLOW, *objs)
    pass

def print_warning(*objs):
    _log(logging.WARNING, colored.fore.RED, *objs)
    pass

def print_error(*objs):
    _log(logging.ERROR, colored.fore.RED+colored.style.BOLD, *objs)
    pass

def printr(*objects):
    print('\033[K'+' '.join(map(str, objects)), end='\r')

def exceptstr(e):
    return f'{e.__class__.__name__}: {e}'

def ratiostr(i, total):
    return f'{i+1:0{len(str(total))}}/{total}'

def ordinal(n):
    return f'{n}{"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4]}'
