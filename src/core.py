#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import sys
from command import Command

def distance(x2 : float, y2 : float, x1=0, y1=0) -> float:
    return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))


def center(input_filename, output_filename, offset=None):
    if offset is None:
        minimum_distance = 0
        minimum_point = None
        with open(input_filename, "r") as input_file:
            for line in input_file.readlines():
                current_command = Command(line)
                if current_command.type is not None:
                    # This is horrible
                    # TODO: Clean this
                    if current_command.state["Z"] == None and current_command.state["X"] != None and current_command.state["Y"] != None:
                        current_distance = distance(current_command.state["X"], current_command.state["Y"])
                        if minimum_point == None and current_distance != 0:
                            # Distance hasn't been modified yet
                            minimum_distance = current_distance
                            minimum_point = current_command.state
                            print(minimum_point)
                        elif minimum_distance > current_distance and current_distance != 0:
                            minimum_distance = current_distance
                            minimum_point = current_command.state
                            print(minimum_point)

        offset = (0 - minimum_point["X"], 0 - minimum_point["Y"])

        del minimum_distance
        del minimum_point
        
    with open(input_filename, "r") as input_file:
        with open(output_filename, "w") as output_file:
            for line in input_file.readlines():
                current_command = Command(line)
                if current_command.type is None:
                    output_file.write(current_command.source)
                else:
                    if current_command.state["Z"] == None and current_command.state["X"] != None and current_command.state["Y"] != None:
                        if current_command.state["X"] != 0.0 and current_command.state["Y"] != 0.0:
                            current_command.state["X"] += offset[0]
                            current_command.state["Y"] += offset[1]
                        output_file.write(str(current_command))
                    else:
                       output_file.write(current_command.source)     
    return offset



'''
minimum_distance = 0
minimum_point = None
with open(sys.argv[1], "r") as input_file:
    for line in input_file.readlines():
        current_command = Command(line)
        if current_command.type is not None:
            # This is horrible
            # TODO: Clean this
            if current_command.state["Z"] == None and current_command.state["X"] != None and current_command.state["Y"] != None:
                current_distance = distance(current_command.state["X"], current_command.state["Y"])
                if minimum_point == None and current_distance != 0:
                    # Distance hasn't been modified yet
                    minimum_distance = current_distance
                    minimum_point = current_command.state
                    print(minimum_point)
                elif minimum_distance > current_distance and current_distance != 0:
                    minimum_distance = current_distance
                    minimum_point = current_command.state
                    print(minimum_point)
            
    
offset_x = 0 - minimum_point["X"]
offset_y = 0 - minimum_point["Y"]

del minimum_distance
del minimum_point

with open(sys.argv[1], "r") as input_file:
    
    with open(sys.argv[2], "w") as output_file:
        for line in input_file.readlines():
            current_command = Command(line)
            if current_command.type is None:
                output_file.write(current_command.source)
            else:
                if current_command.state["Z"] == None and current_command.state["X"] != None and current_command.state["Y"] != None:
                    if current_command.state["X"] != 0.0 and current_command.state["Y"] != 0.0:
                        current_command.state["X"] += offset_x
                        current_command.state["Y"] += offset_y
                    output_file.write(str(current_command))
                else:
                   output_file.write(current_command.source) 

'''
