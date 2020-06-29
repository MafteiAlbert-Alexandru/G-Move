#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import name, path
from interpreter import Interpreter
import core
_PLATFORM_ = name


print(" G - Code Repositioner \n")

def ask_for_master_file():
    print("1. Add master file: \n>", end='')
    file = input()

    return (file, "The file '{[0]}' does not exist")

def ask_for_other_files():
    print("2. Add other files(optional, and must be separated with '\" \"'. ex: '\"test1\" \"test2\"') \n>", end='')
    files = input()
    if files == '':
        return ([], "Some of the files {[0]} do not exist", True)
    else:
        result = [] #map(lambda x: x.replace('"',''), files.split('" "')) <- I like this but it doesn't work
        for i in files.split('" "'):
            result.append(i.replace('"',''))

        return (result, "Some of the files {[0]} do not exist", False)

master_file = Interpreter.repeat_until_result(ask_for_master_file, lambda x: path.isfile(x[0]))
other_files = Interpreter.repeat_until_result(ask_for_other_files, lambda x: True if x[2] else all(map(path.isfile,x[0])))
try:
    other_files.remove(master_file)
except:
    pass

implemented = {"c": core.center}
while(True):
    print("Now, what do you want to do?")
    print("c - Brings(Centers) piece closer")
    print("fp - Flips in place(Not Implemented)")
    print("fh - Flips on horizontal axis(Not Implemented)")
    print("fv - Flips on verical axis(Not Implemented) \n>", end='')

    if input() == "c":
        offset = core.center(master_file, master_file+'.out')

        for i in other_files:
            core.center(i, i+'.out', offset)

    else:
        print("no")