import Prepin_Writer


class ParameterSweeper:
    def __init__(self):
        self.origin = []        # The base model
        self.axes = []          # The parameters that are being swept. This is an array of indexes for the origin
        self.n_steps = []       # The number of steps to take in the respective axis
        self.steps = []         # The step value
        self.sweep = []         # Multidimensional array containing the parameter sweep in row-major order
        self.stride = [1]
        self.dimension_index = [0]

        self.axis_names = []
        self.prepin_writer = Prepin_Writer.PrepinWriter()

    def set_origin(self, dataset):
        self.origin = dataset

    def set_name(self, name):
        self.name = name

    # parameter_list is expected to be a string of comma separated variable names with subscripts in brackets
    def set_axes(self, parameter_string):
        parameter_list = []
        previous_comma = 0
        for i in range(len(parameter_string)):
            if parameter_string[i] == ",":
                parameter_list.append(parameter_string[previous_comma:i])
                previous_comma = i + 1
        parameter_list.append(parameter_string[previous_comma:])
        self.axis_names = parameter_list
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
            stride.append((n + 1) * stride[len(stride)-1])
            dimension_index.append(dimension_index[len(dimension_index)-1] + stride[len(stride)-1])
        print(stride)
        # Sweeping
        self.sweep = [self.origin.copy()]
        for axis in range(len(self.axes)):
            # Make each step
            for step in range(1, self.n_steps[axis]+1):
                for i in range(stride[axis]):
                    print("Axis: " + str(axis) + "\nStep: " + str(step) + "\nStride: " + str(i) + "\nFrom: " + str(i) + "\n")
                    # Copy, edit and append the prepin dataset
                    dataset = self.sweep[i].copy()
                    value = float(dataset[self.axes[axis]][5]) + step * self.steps[axis]
                    dataset[self.axes[axis]][5] = str(value)
                    self.sweep.append(dataset)
        self.stride = stride
        self.dimension_index = dimension_index
        for dataset in self.sweep:
            for axis in self.axes:
                print(dataset[axis][0] + " = " + dataset[axis][5])

    def export_sweep(self, file_address):
        print(len(self.sweep))
        # Exporting each prepin dataset in the parameter sweep
        for dataset in self.sweep:
            sweep_file_address = file_address
            # Appending axis names and values to the file name
            for axis in range(len(self.axes)):
                sweep_file_address = sweep_file_address + "_" + self.axis_names[axis] + "_" + dataset[self.axes[axis]][5]
            self.prepin_writer.set_dataset(dataset)
            self.prepin_writer.write(sweep_file_address)
