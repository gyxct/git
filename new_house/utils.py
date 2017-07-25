# !/usr/bin/env python
# coding=utf-8


import re


def pro_digital(s):
    digit = re.findall(r'\d+', s)
    if digit:
        return digit[0]
    else:
        return '0'


def pro_float(s):
    floats = re.findall(r'\d+.\d*', s)
    if floats:
        return floats[0]
    else:
        return '0'

