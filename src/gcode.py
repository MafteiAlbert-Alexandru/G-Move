from command import Command ,CommandType
import math
import os

class GCodeFile:
    def __init__(self, name):
        self.name = name
        os.rename(name.encode(), (name+"1").encode())
        self.version = 1

    def calculate_bounding_box(self):
        bounding_box = [[999999999,-999999999],[-999999999,-999999999],[-999999999,999999999],[999999999,999999999]]

        with open(self.name+str(self.version), "r") as input_file:
            
            for line in input_file.readlines():
                current_command = Command(line)
                if current_command.type >= CommandType.HORIZONTAL_COMMAND: # Is horizontal or mixed
                    # nightmare, nightmare, nightmare, nightmare, nightmare, nightmare, nightmare, nightmare, nightmare, nightmare, nightmare, nightmare, nightmare, nightmare, nightmare
                    # TODO: Clean this
             
                    if current_command.values["X"] < bounding_box[0][0]:
                        bounding_box[0][0] = current_command.values["X"] 
                    if current_command.values["Y"] > bounding_box[0][1]:
                        bounding_box[0][1] = current_command.values["Y"] 


                    if current_command.values["X"] > bounding_box[1][0]:
                        bounding_box[1][0] = current_command.values["X"] 
                    if current_command.values["Y"] > bounding_box[1][1]:
                        bounding_box[1][1] = current_command.values["Y"]

                    if current_command.values["X"] > bounding_box[2][0]:
                        bounding_box[2][0] = current_command.values["X"] 
                    if current_command.values["Y"] < bounding_box[2][1]:
                        bounding_box[2][1] = current_command.values["Y"]

                    if current_command.values["X"] < bounding_box[3][0]:
                        bounding_box[3][0] = current_command.values["X"] 
                    if current_command.values["Y"] < bounding_box[3][1]:
                        bounding_box[3][1] = current_command.values["Y"]

        return bounding_box
    @staticmethod
    def distance(x2 : float, y2 : float, x1=0, y1=0) -> float:
        return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

    def center(self, offset = None):
        if offset is None:
            minimum_distance = 0
            minimum_point = None
            with open(self.name + str(self.version), "r") as input_file:
                for line in input_file.readlines():
                    current_command = Command(line)
                    if current_command.type >= CommandType.HORIZONTAL_COMMAND: # Is horizontal or mixed
                        current_distance = self.distance(current_command.values["X"], current_command.values["Y"])
                        if current_distance != 0:
                            if minimum_point == None:
                            # Distance hasn't been modified yet
                                minimum_distance = current_distance
                                minimum_point = current_command.values

                            elif minimum_distance > current_distance:
                                minimum_distance = current_distance
                                minimum_point = current_command.values                  

            offset = (-minimum_point["X"], -minimum_point["Y"])

            del minimum_distance
            del minimum_point
                
            with open(self.name + str(self.version), "r") as input_file:
                with open(self.name + str(self.version+1), "w+") as output_file:
                    for line in input_file.readlines():
                        current_command = Command(line)

                        if current_command.type >= CommandType.HORIZONTAL_COMMAND:
                            current_command.values["X"] += offset[0]
                            current_command.values["Y"] += offset[1]
                        output_file.write(str(current_command))
        self.version += 1
        return offset

    def flip_horizontally(self, bounding_box = None):
        if bounding_box is None:
            bounding_box = self.calculate_bounding_box()

        with open(self.name+str(self.version), "r") as input_file:
            with open(self.name + str(self.version+1), "w+") as output_file:
                for line in input_file.readlines():
                    current_command = Command(line)
                    if current_command.type >= CommandType.HORIZONTAL_COMMAND:
                        current_command.values["X"] += ((bounding_box[1][0]-bounding_box[0][0])/2 - current_command.values["X"]) * 2
                    output_file.write(str(current_command))
        self.version += 1
        return bounding_box
    
    def flip_vertically(self, bounding_box = None):
        if bounding_box is None:
            bounding_box = self.calculate_bounding_box()

        with open(self.name+str(self.version), "r") as input_file:
            with open(self.name + str(self.version+1), "w+") as output_file:
                for line in input_file.readlines():
                    current_command = Command(line)
                    if current_command.type >= CommandType.HORIZONTAL_COMMAND:
                        current_command.values["Y"] += ((bounding_box[0][1]-bounding_box[3][1])/2 - current_command.values["Y"]) * 2
                    output_file.write(str(current_command))
        self.version += 1  
        return bounding_box