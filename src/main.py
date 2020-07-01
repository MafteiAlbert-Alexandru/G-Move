#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path
from interpreter import Interpreter
from gcode import GCodeFile

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

master_file = GCodeFile(Interpreter.repeat_until_result(ask_for_master_file, lambda x: path.isfile(x[0])))
other_files = map(GCodeFile,  Interpreter.repeat_until_result(ask_for_other_files, lambda x: True if x[2] else all(map(path.isfile,x[0]))))

try:
    other_files.remove(master_file)
except:
    pass

while(True):
    print("Now, what do you want to do?")
    print("c - Brings(Centers) piece closer")
    print("fph - Flips in place horizontally")
    print("fpv - Flips in place vertically")
    print("q - Quit")
    command = input()
    if command == "c":
        offset = master_file.center()

        for i in other_files:
            i.center(offset)

    elif command == "fph":
        bounding_box = master_file.flip_horizontally()

        for i in other_files:
            i.flip_horizontally(bounding_box)
    
    elif command == "fpv":
        bounding_box = master_file.flip_vertically()

        for i in other_files:
            i.flip_vertically(bounding_box)

    elif command == "q":
        quit(0)