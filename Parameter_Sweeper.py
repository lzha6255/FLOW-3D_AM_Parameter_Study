class ParameterSweeper:
    def __init__(self):
        self.origin = []        # The base model
        self.axes = []          # The parameters that are being swept. This is an array of indexes for the origin
        self.n_steps = []       # The number of steps to take in the respective axis
        self.steps = []         # The step value
        self.sweep = []         # Multidimensional array containing the parameter sweep in row-major order

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
    def set_steps(self, parameter_steps, n_steps):
        previous_comma = 0
        for i in range(len(parameter_steps)):
            if parameter_steps[i] == ",":
                self.steps.append(float(parameter_steps[previous_comma:i]))
                previous_comma = i + 1
        self.steps.append(float(parameter_steps[previous_comma:]))
        previous_comma = 0
        for i in range(len(n_steps)):
            if n_steps[i] == ",":
                self.n_steps.append(int(n_steps[previous_comma:i]))
                previous_comma = i + 1
        self.n_steps.append(int(n_steps[previous_comma:]))
        print(self.steps)
        print(self.n_steps)

    def parameter_sweep(self):
        print("Sweeping Parameters")
        # The sweep may be multidimensional, this array stores the strides in each dimension
        stride = [1]
        # Array to store the index where each dimension starts
        dimension_index = [0]
        for n in self.n_steps:
            stride.append(n * stride[len(stride)-1])
            dimension_index.append(dimension_index[len(dimension_index)-1] + stride[len(stride)-1])
        print(stride)
        # Sweeping
        self.sweep = [self.origin.copy()]
        for axis in range(len(self.axes)):
            # Make each step
            for step in range(1, self.n_steps[axis]+1):
                for i in range(stride[axis]):
                    # Copy, edit and append the prepin dataset
                    dataset = self.sweep[dimension_index[axis]+i].copy()
                    value = float(dataset[self.axes[axis]][5]) + step * self.steps[axis]
                    dataset[self.axes[axis]][5] = str(value)
                    self.sweep.append(dataset)
        print(self.sweep)
