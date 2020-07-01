# MIT License
#
# Copyright (c) 2020 NightChips64
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# -*- coding: utf-8 -*-
from enum import Enum


class CommandType(Enum):
    SETUP_COMMAND = 0
    VERTICAL_COMMAND = 1
    HORIZONTAL_COMMAND = 2
    MIXED_COMMAND = 3    

    def __eq__(self, other):    
        return self.value == other.value

    def __ge__(self, other):
        return self.value >= other.value



class Command:

    def __init__(self, line):
        self.command = None
        self.values = {"X": None, "Y": None, "Z": None}
        self.type = CommandType.SETUP_COMMAND
        self.source = line

        if line.startswith("F"):
            # We can ignore this command in many cases
            # TODO: Verify the use of F command
            self.command = line[0:3]
            self.type = CommandType.SETUP_COMMAND

        elif line.startswith("M"):
            # We can ignore this command in many cases
            # TODO: Verify the use of M command
            self.command = line[0:3]
            self.type = CommandType.SETUP_COMMAND

        elif line.startswith("G"):
            self.command = line[0:3]
            line = line[3:]
            inserting = None
            current_digits = []
            
            for index in range(len(line)):
                char = line[index]
                if inserting is not None:
                    current_digits.append(char)

                    
                if char in self.values.keys():
                    
                    if current_digits != []:
                        self.values[inserting] = float(''.join(current_digits[:-1]))
                        current_digits=[]
                    inserting = char
            try:
                self.values[inserting] = float(''.join(current_digits))
            except:
                pass  
            
            if self.values["X"] is None and \
                self.values["Y"] is None and \
                self.values["Z"] is None:
                
                self.type = CommandType.SETUP_COMMAND

            elif self.values["X"] is None and \
                self.values["Y"] is None and \
                self.values["Z"] is not None:

                self.type = CommandType.VERTICAL_COMMAND

            elif self.values["X"] is not None and \
                self.values["Y"] is not None and \
                self.values["Z"] is None:

                self.type = CommandType.HORIZONTAL_COMMAND
            
            else: 
                self.type = CommandType.MIXED_COMMAND
  
    def __str__(self):
        if self.type == CommandType.SETUP_COMMAND:
            return self.source
        elif  self.type == CommandType.VERTICAL_COMMAND:
            return self.source

        string_format = self.command + " "
        string_format += ("X" + "{0:.4f}".format(self.values["X"])) if self.values["X"] != None else "" 
        string_format += ("Y" + "{0:.4f}".format(self.values["Y"])) if self.values["Y"] != None else "" 
        string_format += ("Z" + "{0:.4f}".format(self.values["Z"])) if self.values["Z"] != None else "" + "\n"
        return string_format

