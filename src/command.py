class Command:

    def __init__(self, line):
        self.state = {"X": None, "Y": None, "Z": None}
        self.type = None
        self.source = line

        if line.startswith("F"):
            # We can ignore this command in many cases
            # TODO: Verify the use of F command
            pass

        elif line.startswith("M"):
            # We can ignore this command in many cases
            # TODO: Verify the use of M command
            pass

        elif line.startswith("G"):
            self.type = line[0:3]
            line = line[3:]
            inserting = None
            current_digits = []
            
            for index in range(len(line)):
                char = line[index]
                if inserting is not None:
                    current_digits.append(char)

                    
                if char in self.state.keys():
                    
                    if current_digits != []:
                        self.state[inserting] = float(''.join(current_digits[:-1]))
                        current_digits=[]
                    inserting = char
            try:
                self.state[inserting] = float(''.join(current_digits))
            except:
                pass  


    def __str__(self):
        string_format = self.type + " "
        string_format += ("X" + "{0:.4f}".format(self.state["X"])) if self.state["X"] != None else "" 
        string_format += ("Y" + "{0:.4f}".format(self.state["Y"])) if self.state["Y"] != None else "" 
        string_format += ("Z" + "{0:.4f}".format(self.state["Z"])) if self.state["Z"] != None else "" + "\n"
        return string_format

