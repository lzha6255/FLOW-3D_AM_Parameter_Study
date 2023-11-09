class ParameterSweeper:
    def __init__(self):
        self.origin = []        # The base model
        self.axes = []          # The parameters that are being swept. This is an array of indexes for the origin
        self.steps = []         # The steps over which the sweep occurs
        self.sweep = []         # Multidimensional array containing the parameter sweep

    def set_origin(self, dataset):
        self.origin = dataset

    # parameter_list is expected to be a string of comma separated variable names with subscripts in brackets
    def set_axes(self, parameter_string):
        parameter_list = []
        previous_comma = 0
        for i in range(len(parameter_string)):
            if parameter_string[i] == ",":
                parameter_list.append(parameter_string[previous_comma:i])
                previous_comma = i + 1
        parameter_list.append(parameter_string[previous_comma:])
        print(parameter_list)
        # Search the origin for the parameter
        for parameter in parameter_list:
            # Separate the name and subscript if there is a subscript
            subscript = ""
            name = parameter
            if parameter[len(parameter)-1] == ")":
                for i in range(len(parameter)-1, 0, -1):
                    if parameter[i] == "(":
                        subscript = parameter[i+1:len(parameter)-1]
                        name = parameter[:i]
            match = False
            for i in range(len(self.origin)):
                # Check for name and subscript match
                if name.lower() == self.origin[i][0].lower() and subscript == self.origin[i][1]:
                    # Set the index of the parameter to sweep
                    self.axes.append(i)
                    match = True
            if not match:
                print("Could not find parameter " + parameter + " in origin.")
        print(self.axes)

    # parameter_steps is expected to be a string of comma separated numerical values
    def set_steps(self, parameter_steps):
        previous_comma = 0
        for i in range(len(parameter_steps)):
            if parameter_steps[i] == ",":
                self.steps.append(float(parameter_steps[previous_comma:i]))
                previous_comma = i + 1
        self.steps.append(float(parameter_steps[previous_comma:]))
        print(self.steps)

    def sweep(self):
        # All required data must be set
        if not(len(self.origin) and len(self.axes) and len(self.steps)):
            return
        # There must be a step specified for each axis
        if not(len(self.axes) == len(self.steps)):
            return

