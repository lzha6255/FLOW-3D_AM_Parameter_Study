from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

import csv


class PrepinFileTool:
    def __init__(self):
        self.prepin_variable_arrays = []
        self.variable_dictionary = []
        self.block_dictionary = []
        self.variable_dictionary_header = ["NAME", "SUBSCRIPT", "DEFAULT_VALUE", "DESCRIPTION", "DIMENSIONS"]
        self.block_dictionary_header = ["NAMELIST", "", "DESCRIPTION", "REQUIRED"]
        self.file_address = ""
        self.filenames = []
        self.unit_systems = [{"M": "g", "L": "cm", "T": "K", "t": "s", "Q": "scoul"}]

        self.root = Tk()
        self.root.title("FLOW-3D prepin file tool")
        self.root.geometry("1000x500")

        self.menu = Menu(self.root)

        # File menu
        self.file_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Load block dictionary", command=self.select_block_name_file)
        self.file_menu.add_command(label="Load variable dictionary", command=self.select_variable_name_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=exit)

        # Save menu
        self.save_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Save", menu=self.save_menu)
        self.save_menu.add_command(label="Save block dictionary as .csv", command=self.save_block_dictionary)
        self.save_menu.add_command(label="Save variable dictionary as .csv", command=self.save_variable_dictionary)

        # TODO Unit system menu

        self.label_message = Label(self.root, text="A tool for tracking and making changes to prepin.* files")
        self.label_block_names_loaded = Label(self.root, text="No block name dictionary loaded", foreground="red")
        self.label_variable_names_loaded = Label(self.root, text="No variable name dictionary loaded", foreground="red")
        self.label_prepin_file_selector = Label(self.root, text="Select active prepin.* files")

        # Combo boxes for selecting prepin files
        self.combobox_prepin_1 = Combobox(self.root, values=[])
        self.combobox_prepin_2 = Combobox(self.root, values=[])
        self.combobox_prepin_1.set("No prepin.* files loaded")
        self.combobox_prepin_2.set("No prepin.* files loaded")

        self.label_block_names_loaded.grid(row=0, column=0)
        self.label_variable_names_loaded.grid(row=1, column=0)
        self.label_prepin_file_selector.grid(row=2, column=0)
        self.combobox_prepin_1.grid(row=3, column=0)
        self.combobox_prepin_2.grid(row=4, column=0)
        self.label_message.grid(row=5, column=0)

        self.root.config(menu=self.menu)

    def start(self):
        self.root.mainloop()

    def select_block_name_file(self):
        self.file_address = filedialog.askopenfilename(title="Select a block name dictionary (.txt)",
                                                       filetypes=(("text files (.txt)", "*.txt*"),
                                                                  ("all files", "*.*")))
        if not(len(self.file_address)):
            return
        self.label_message.configure(text="Opened: " + self.file_address)
        self.block_dictionary = self.read_dictionary(self.block_dictionary_header, self.file_address)
        print(self.block_dictionary)
        self.label_block_names_loaded.configure(text="Block name dictionary loaded", foreground="green")

    def select_variable_name_file(self):
        self.file_address = filedialog.askopenfilename(title="Select a variable name dictionary (.txt)",
                                                       filetypes=(("text files (.txt)", "*.txt*"),
                                                                  ("all files", "*.*")))
        if not(len(self.file_address)):
            return
        self.label_message.configure(text="Opened: " + self.file_address)
        self.variable_dictionary = self.read_dictionary(self.variable_dictionary_header, self.file_address)
        print(self.variable_dictionary)
        self.label_variable_names_loaded.configure(text="Variable name dictionary loaded", foreground="green")

    def save_block_dictionary(self):
        if not(len(self.block_dictionary)):
            # TODO change invalid action messages to be pop up windows
            self.label_message.configure(text="No block dictionary to save", foreground="red")
            return
        self.file_address = filedialog.asksaveasfilename(title="Save block dictionary as",
                                                         filetypes=([("csv file (.csv)", "*.csv*")]))
        self.add_csv_file_extension()
        with open(self.file_address, "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(self.block_dictionary)
        self.label_message.configure(text="Saved block dictionary to "+self.file_address, foreground="black")

    def save_variable_dictionary(self):
        if not(len(self.variable_dictionary)):
            self.label_message.configure(text="No variable dictionary to save", foreground="red")
            return
        self.file_address = filedialog.asksaveasfilename(title="Save variable dictionary as",
                                                         filetypes=([("csv file (.csv)", "*.csv")]))
        self.add_csv_file_extension()
        with open(self.file_address, "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(self.variable_dictionary)
        self.label_message.configure(text="Saved variable dictionary as "+self.file_address, foreground="black")

    def read_dictionary(self, header, file_name):
        fp = open(file_name, "r")

        line = fp.readline()
        line_number = 1
        rows = []
        row = header

        while line:
            # "*" indicates the start of an entry, so the column number is now tracked.
            if len(line) > 7 and line[3:6] == "* -":
                if not (row[0] == "NAME" or row[0] == "NAMELIST") or len(rows) == 0:
                    rows.append(row)
                    print("Appending row at line number " + str(line_number))
                row = []

            # Each field in a dictionary entry is preceded by a hyphen.
            if len(line) > 6 and line[5:7] == "- ":
                if len(line) < 16 or not (line[7:15] == ":envvar:"):
                    row.append(line[7:len(line) - 1])
                # Variable names are preceded by ":envvar:" and surrounded by backticks.
                else:
                    # Sometimes the variable name may have a subscript in brackets
                    if line[len(line) - 3] == ")":
                        for i in range(len(line)):
                            if line[i] == "(":
                                row.append(line[16:i])
                                row.append(line[i + 1:len(line) - 3])
                                break
                    # Non subscripted case
                    else:
                        row.append(line[16:len(line) - 2])
                        row.append("")

            line = fp.readline()
            line_number = line_number + 1

        fp.close()
        return rows

    def read_prepin_file(self, prepin_file_name):
        rows = [["NAME", "SUBSCRIPT", "DEFAULT_VALUE", "DESCRIPTION", "UNITS", "SET_VALUE", "REMARK"]]
        row = []

        prepin_file_name = "prepin_files\\" + prepin_file_name + ".txt"
        fp = open(prepin_file_name, "r")

        line = " "

        while line:
            line = fp.readline()

            # An ampersand as the second character indicates the line contains a block name.
            if len(line) > 2 and line[1] == "&":
                # Searching the dictionary.
                for i in range(len(self.block_dictionary)):
                    if line[2:len(line) - 1].lower() == self.block_dictionary[i][0].lower():
                        row = [self.block_dictionary[i][0], "BLOCK", "BLOCK", self.block_dictionary[i][2], "BLOCK", "BLOCK", "BLOCK"]
                        break
                # Case where dictionary entry is missing.
                if len(row) == 0:
                    row = [line[2:len(line) - 1], "BLOCK", "BLOCK", "MISSING DESCRIPTION", "BLOCK", "BLOCK", "BLOCK"]

            # A tabbed line indicates a variable value.
            if len(line) > 4 and line[:4] == "    ":
                var_name = ""
                value = ""
                subscript = ""
                remark = ""
                # Variable names and values are separated by a "=".
                # Also checking for a subscript in brackets.
                for i in range(4, len(line)):
                    if line[i] == "(":
                        var_name = line[4:i]
                        for j in range(i, len(line)):
                            if line[j] == ")":
                                subscript = line[i + 1:j]
                                break
                    if line[i] == "=":
                        if not (len(var_name)):
                            var_name = line[4:i]
                        # Variable lines always end with ",\n".
                        for j in range(i, len(line)):
                            # End of the value indicated by a comma. After the comma we may have a remark.
                            if line[j] == ",":
                                value = line[i + 1:j]
                                remark = line[j + 1:len(line) - 2]
                                break
                        break
                # Removing "remark=" from the remark.
                for i in range(len(remark)):
                    if remark[i] == "=":
                        remark = remark[i + 1:]
                        break
                # Remarks are not considered variables.
                if var_name == "remark":
                    continue
                row = [var_name, "MISSING SUBSCRIPT DESCRIPTION", "MISSING DEFAULT VALUE", "MISSING DESCRIPTION",
                       "MISSING UNITS"]
                # Searching the dictionary.
                for i in range(len(self.variable_dictionary)):
                    if var_name.lower() == self.variable_dictionary[i][0].lower():
                        # Case where a generic expression is given for the units.
                        if (len(self.variable_dictionary[i]) > 4 and len(self.variable_dictionary[i][4]) and
                                self.variable_dictionary[i][4][0] == "["):
                            generic_units = self.variable_dictionary[i][4].replace("\ :sup:", "^")
                            units = ""
                            # TODO switchable unit system
                            keys = list(self.unit_systems[0])
                            for j in range(1, len(generic_units) - 1):
                                if generic_units[j] in keys:
                                    units = units + self.unit_systems[0][generic_units[j]]
                                # Remove backticks
                                elif generic_units[j] == "`":
                                    continue
                                else:
                                    units = units + generic_units[j]
                            row = self.variable_dictionary[i][:4].copy()
                            row.append(units)
                        else:
                            row = self.variable_dictionary[i].copy()
                        # Filling out the row so that it contains at least 5 elements.
                        while len(row) < 5:
                            row.append("")
                        break
                row[1] = subscript
                row.append(value)
                row.append(remark)

            if len(row):
                rows.append(row)
                row = []

        fp.close()

    def add_csv_file_extension(self):
        if not(self.file_address[len(self.file_address)-4:] == ".csv"):
            self.file_address = self.file_address + ".csv"
