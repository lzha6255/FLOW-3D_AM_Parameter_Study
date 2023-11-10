from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *

import csv

import Table_Window
import Prepin_Writer
import Parameter_Sweeper


class PrepinFileTool:
    def __init__(self):
        self.prepin_files = []
        self.variable_dictionary = []
        self.block_dictionary = []
        self.variable_dictionary_header = ["NAME", "SUBSCRIPT", "DEFAULT_VALUE", "DESCRIPTION", "DIMENSIONS"]
        self.block_dictionary_header = ["NAMELIST", "", "DESCRIPTION", "REQUIRED"]
        self.file_address = ""
        self.prepin_file_name_index = {}
        self.unit_system_index = {"CGS": 0}
        self.unit_systems = [{"M": "g", "L": "cm", "T": "K", "t": "s", "Q": "scoul"}]
        self.n_prepin_file_selections = 2
        self.delta = []
        self.prepin_writer = Prepin_Writer.PrepinWriter()
        self.parameter_sweeper = Parameter_Sweeper.ParameterSweeper()

        self.root = Tk()
        self.root.title("FLOW-3D prepin file tool")
        self.root.geometry("1000x500")

        self.menu = Menu(self.root)

        # File menu
        self.file_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Load previous session", command=self.select_session)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Load block dictionary", command=self.select_block_name_file)
        self.file_menu.add_command(label="Load variable dictionary", command=self.select_variable_name_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Load prepin.* file", command=self.select_prepin_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=exit)

        # Save menu
        self.save_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Save", menu=self.save_menu)
        self.save_menu.add_command(label="Save session", command=self.save_session)
        self.save_menu.add_separator()
        self.save_menu.add_command(label="Save block dictionary as .csv", command=self.save_block_dictionary)
        self.save_menu.add_command(label="Save variable dictionary as .csv", command=self.save_variable_dictionary)
        self.save_menu.add_separator()
        self.save_prepin_submenu = Menu(self.menu, tearoff=0)
        self.save_menu.add_cascade(label="Save prepin file as .csv", menu=self.save_prepin_submenu)

        # Display menu
        self.display_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Display", menu=self.display_menu)
        self.display_menu.add_command(label="Block Dictionary", command=self.display_block_dictionary)
        self.display_menu.add_command(label="Variable Dictionary", command=self.display_variable_dictionary)
        self.display_menu.add_separator()
        self.display_prepin_submenu = Menu(self.menu, tearoff=0)
        self.display_menu.add_cascade(label="prepin.* file", menu=self.display_prepin_submenu)
        self.display_menu.add_separator()
        self.display_menu.add_command(label="Delta", command=self.display_delta)

        # Export menu
        self.export_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Export", menu=self.export_menu)
        self.export_prepin_submenu = Menu(self.menu, tearoff=0)
        self.export_menu.add_cascade(label="prepin.* file", menu=self.export_prepin_submenu)

        # Unit system selection
        self.frame_unit_system = Frame(self.root, padding=5)
        self.label_unit_system = Label(self.frame_unit_system, text="Unit System: ")
        self.unit_system = StringVar()
        self.combobox_unit_system = Combobox(self.frame_unit_system, values=["CGS"], textvariable=self.unit_system)
        self.combobox_unit_system.set("Select a unit system")
        self.label_unit_system.pack(side=LEFT)
        self.combobox_unit_system.pack(side=LEFT)

        # System message
        self.label_message = Label(self.root, text="A tool for tracking and making changes to prepin.* files")
        # Dictionary state descriptors
        self.label_block_names_loaded = Label(self.root, text="No block name dictionary loaded", foreground="red")
        self.label_variable_names_loaded = Label(self.root, text="No variable name dictionary loaded", foreground="red")

        # Combo boxes for selecting prepin files
        self.frame_prepin_selector = Frame(self.root, padding=5)
        self.label_prepin_selector = Label(self.frame_prepin_selector, text="prepin.* file selection: ")
        self.label_prepin_selector.pack(anchor=W, side=TOP)
        self.comboboxes_prepin_selection = []
        for i in range(self.n_prepin_file_selections):
            self.comboboxes_prepin_selection.append(Combobox(self.frame_prepin_selector, values=[]))
            self.comboboxes_prepin_selection[i].set("No prepin.* files loaded")
            self.comboboxes_prepin_selection[i].pack(side=TOP)

        # Buttons to clear data
        self.frame_clear_data = Frame(self.root, padding=5)
        self.button_clear_prepin_data = Button(self.frame_clear_data, text="Clear prepin data",
                                               command=self.callback_clear_prepin_data)
        self.button_clear_all_data = Button(self.frame_clear_data, text="Clear all data",
                                            command=self.callback_clear_all)
        self.button_clear_all_data.pack(side=RIGHT)
        self.button_clear_prepin_data.pack(side=RIGHT)

        # Delta
        self.frame_delta = Frame(self.root, padding=5)
        self.button_calculate_delta = Button(self.frame_delta, text="Calculate delta between selected prepin data",
                                             command=self.calculate_delta)
        self.button_display_delta = Button(self.frame_delta, text="Display delta in table", command=self.display_delta)
        self.button_calculate_delta.pack(side=LEFT)
        self.button_display_delta.pack(side=LEFT)

        # Parameter Sweep Entry Boxes
        self.frame_sweep = Frame(self.root, padding=5)
        self.parameter_var = StringVar()
        self.step_var = StringVar()
        self.n_steps_var = StringVar()
        self.label_parameter = Label(self.frame_sweep, text="Parameters to Sweep:")
        self.label_step = Label(self.frame_sweep, text="Parameter Steps:")
        self.label_n_steps = Label(self.frame_sweep, text="Number of Steps:")
        self.entry_parameters = Entry(self.frame_sweep, textvariable=self.parameter_var)
        self.entry_steps = Entry(self.frame_sweep, textvariable=self.step_var)
        self.entry_n_steps = Entry(self.frame_sweep, textvariable=self.n_steps_var)
        self.button_sweep = Button(self.frame_sweep, text="Sweep Parameters", command=self.parameter_sweep)
        self.label_parameter.pack(side=TOP)
        self.entry_parameters.pack(side=TOP)
        self.label_step.pack(side=TOP)
        self.entry_steps.pack(side=TOP)
        self.label_n_steps.pack(side=TOP)
        self.entry_n_steps.pack(side=TOP)
        self.button_sweep.pack(side=TOP)

        # Placing right side widgets and frames
        self.frame_clear_data.pack(anchor=NE, side=RIGHT)

        # Placing top side widgets and frames
        self.frame_unit_system.pack(anchor=NW, side=TOP)
        self.frame_prepin_selector.pack(anchor=NW, side=TOP)
        self.frame_delta.pack(anchor=NW, side=TOP)
        self.frame_sweep.pack(anchor=NW, side=TOP)

        # Placing bottom side widgets and frames
        self.label_message.pack(anchor=SW, side=BOTTOM)
        self.label_variable_names_loaded.pack(anchor=SW, side=BOTTOM)
        self.label_block_names_loaded.pack(anchor=SW, side=BOTTOM)

        self.root.config(menu=self.menu)

    def start(self):
        self.root.mainloop()

    def select_block_name_file(self):
        self.file_address = ""
        self.file_address = filedialog.askopenfilename(title="Select a block name dictionary (.txt)",
                                                       filetypes=(("text files (.txt)", "*.txt*"),
                                                                  ("all files", "*.*")))
        if not(len(self.file_address)):
            return
        self.block_dictionary = self.read_dictionary(self.block_dictionary_header, self.file_address)
        self.label_message.configure(text="Opened: "+self.file_address)
        print(self.block_dictionary)
        self.label_block_names_loaded.configure(text="Block name dictionary loaded", foreground="green")

    def select_variable_name_file(self):
        self.file_address = ""
        self.file_address = filedialog.askopenfilename(title="Select a variable name dictionary (.txt)",
                                                       filetypes=(("text files (.txt)", "*.txt*"),
                                                                  ("all files", "*.*")))
        if not(len(self.file_address)):
            return
        self.variable_dictionary = self.read_dictionary(self.variable_dictionary_header, self.file_address)
        self.label_message.configure(text="Opened: " + self.file_address)
        print(self.variable_dictionary)
        self.label_variable_names_loaded.configure(text="Variable name dictionary loaded", foreground="green")

    def select_prepin_file(self):
        if not(len(self.block_dictionary) and len(self.variable_dictionary)):
            messagebox.showerror(title="Could not read prepin.* file",
                                 message="A dictionary is missing. Please ensure both dictionaries are loaded.")
            return
        keys = list(self.unit_system_index)
        if not(self.unit_system.get() in keys):
            messagebox.showerror(title="Could not read prepin.* file",
                                 message="Please select a valid unit system from the drop down menu.")
            return
        self.file_address = ""
        self.file_address = filedialog.askopenfilename(title="Select a prepin file (prepin.*)",
                                                       filetypes=(("prepin files (prepin.*)", "*prepin.*"),
                                                                  ("all files", "*.*")))
        if not(len(self.file_address)):
            return
        # Extracting the name of the prepin file, that is the text after "prepin."
        prepin_file_name = ""
        for i in range(7, len(self.file_address)):
            if self.file_address[i-7:i] == "prepin.":
                prepin_file_name = self.file_address[i:]
        if not(len(prepin_file_name)):
            messagebox.showerror(title="Could not read prepin.* file",
                                 message="It appears the file you selected is not a prepin file. Please select a prepin file or rename your file so that it begins with \"prepin.\"")
            return
        self.prepin_files.append(self.read_prepin_file(self.file_address))
        self.prepin_file_name_index[prepin_file_name] = len(self.prepin_file_name_index)
        for combobox in self.comboboxes_prepin_selection:
            combobox.configure(values=list(self.prepin_file_name_index))
            # Change the combo box text if this is the first prepin file that has been loaded
            if len(self.prepin_file_name_index) == 1:
                combobox.set("Select a prepin file")
        self.label_message.configure(text="Opened: "+self.file_address)
        # Adding new save option to the save prepin submenu
        self.save_prepin_submenu.add_command(label=prepin_file_name,
                                             command=lambda j=self.prepin_file_name_index[prepin_file_name], file_name=prepin_file_name: self.save_prepin(j, file_name))
        # Adding new display option to the display prepin submenu
        self.display_prepin_submenu.add_command(label=prepin_file_name,
                                                command=lambda j=self.prepin_file_name_index[prepin_file_name], file_name=prepin_file_name: self.display_prepin(j, file_name))
        # Adding new export option to the export prepin submenu
        self.export_prepin_submenu.add_command(label=prepin_file_name,
                                               command=lambda j=self.prepin_file_name_index[prepin_file_name], file_name=prepin_file_name: self.export_prepin(j, file_name))

    def select_session(self):
        # Confirmation box only appears if a dictionary has been loaded
        if (len(self.block_dictionary) or len(self.variable_dictionary)) and not(messagebox.askyesno(title="Confirm overwrite", message="Loading a session will overwrite all of the currently loaded data. Do you wish to proceed?")):
            return
        self.file_address = ""
        self.file_address = filedialog.askopenfilename(title="Select a previously saved session",
                                                       filetypes=([("csv file (.csv)", "*.csv*")]))
        if not(len(self.file_address)):
            return
        self.clear_all()
        with open(self.file_address, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            # Mode 0 => unvalidated session file, 1 => block dictionary, 2 => variable dictionary, 3 => prepin data
            # -1 => validated session file but not in write mode
            mode = 0
            for row in csvreader:
                if mode == 1:
                    self.block_dictionary.append(row)
                elif mode == 2:
                    self.variable_dictionary.append(row)
                elif mode == 3:
                    # Rows are always appended to the last prepin file
                    self.prepin_files[len(self.prepin_files)-1].append(row)
                # Switching to write modes only done after the session file has been validated
                if mode:
                    if row[0] == "BLOCK DICTIONARY":
                        self.modal_pop(mode)
                        mode = 1
                    elif row[0] == "VARIABLE DICTIONARY":
                        self.modal_pop(mode)
                        mode = 2
                    elif row[0] == "PREPIN FILE":
                        self.modal_pop(mode)
                        mode = 3
                        self.prepin_files.append([])
                        self.prepin_file_name_index[row[1]] = len(self.prepin_file_name_index)
                else:
                    # File validation
                    if row[0] == "PREPIN FILE TOOL SESSION":
                        mode = -1
        # Configure prepin combo boxes and save/display/export menu if prepin files have been loaded
        if len(self.prepin_file_name_index):
            prepin_file_names = list(self.prepin_file_name_index)
            for combobox in self.comboboxes_prepin_selection:
                combobox.configure(values=prepin_file_names)
                combobox.set("Select a prepin file")
            for name in prepin_file_names:
                self.save_prepin_submenu.add_command(label=name, command=lambda j=self.prepin_file_name_index[name], file_name=name: self.save_prepin(j, file_name))
                self.display_prepin_submenu.add_command(label=name, command=lambda j=self.prepin_file_name_index[name], file_name=name: self.display_prepin(j, file_name))
                self.export_prepin_submenu.add_command(label=name, command=lambda j=self.prepin_file_name_index[name], file_name=name: self.export_prepin(j, file_name))
        self.label_message.configure(text="Session loaded from "+self.file_address)
        if len(self.block_dictionary):
            self.label_block_names_loaded.configure(text="Block name dictionary loaded", foreground="green")
        if len(self.variable_dictionary):
            self.label_variable_names_loaded.configure(text="Variable name dictionary loaded", foreground="green")

    # Pops last item of block dictionary, variable dictionary or prepin file list based off of the number (mode) passed
    # in. 1 = block dictionary, 2 = variable dictionary, 3 = prepin file list. If mode = 3, the last item of the last
    # item in prepin file list is popped.
    def modal_pop(self, mode):
        if mode == 1:
            self.block_dictionary.pop()
        elif mode == 2:
            self.variable_dictionary.pop()
        elif mode == 3:
            self.prepin_files[len(self.prepin_files)-1].pop()

    def save_block_dictionary(self):
        if not(len(self.block_dictionary)):
            messagebox.showerror(title="Dictionary not saved",
                                 message="No data has been loaded. Please load a block dictionary.")
            return
        self.file_address = ""
        self.file_address = filedialog.asksaveasfilename(title="Save block dictionary as",
                                                         filetypes=([("csv file (.csv)", "*.csv*")]))
        if not(len(self.file_address)):
            return
        self.add_csv_file_extension()
        with open(self.file_address, "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(self.block_dictionary)
        self.label_message.configure(text="Saved block dictionary to "+self.file_address, foreground="black")

    def save_variable_dictionary(self):
        if not(len(self.variable_dictionary)):
            messagebox.showerror(title="Dictionary not saved",
                                 message="No data has been loaded. Please load a variable dictionary.")
            return
        self.file_address = ""
        self.file_address = filedialog.asksaveasfilename(title="Save variable dictionary as",
                                                         filetypes=([("csv file (.csv)", "*.csv")]))
        if not(len(self.file_address)):
            return
        self.add_csv_file_extension()
        with open(self.file_address, "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(self.variable_dictionary)
        self.label_message.configure(text="Saved variable dictionary as "+self.file_address, foreground="black")

    def save_prepin(self, i, name):
        self.file_address = ""
        self.file_address = filedialog.asksaveasfilename(title="Save "+name+" as",
                                                         filetypes=([("csv file (.csv)", "*.csv*")]), initialfile=name)
        if not(len(self.file_address)):
            return
        self.add_csv_file_extension()
        with open(self.file_address, "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(self.prepin_files[i])
        self.label_message.configure(text="Saved "+name+" as "+self.file_address, foreground="black")

    def save_session(self):
        self.file_address = ""
        self.file_address = filedialog.asksaveasfilename(title="Save session as",
                                                         filetypes=([("csv file (.csv)", "*.csv*")]))
        if not(len(self.file_address)):
            return
        self.add_csv_file_extension()
        with open(self.file_address, "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["PREPIN FILE TOOL SESSION"])
            if len(self.block_dictionary):
                csvwriter.writerow(["BLOCK DICTIONARY"])
                csvwriter.writerows(self.block_dictionary)
            if len(self.variable_dictionary):
                csvwriter.writerow(["VARIABLE DICTIONARY"])
                csvwriter.writerows(self.variable_dictionary)
            for prepin_file_name in list(self.prepin_file_name_index):
                csvwriter.writerow(["PREPIN FILE", prepin_file_name])
                csvwriter.writerows(self.prepin_files[self.prepin_file_name_index[prepin_file_name]])

    def display_block_dictionary(self):
        block_dictionary_window = Table_Window.TableWindow(self.root, "Block Name Dictionary")
        if block_dictionary_window.load_table(self.block_dictionary):
            block_dictionary_window.grab_set()
        else:
            block_dictionary_window.destroy()

    def display_variable_dictionary(self):
        variable_dictionary_window = Table_Window.TableWindow(self.root, "Variable Name Dictionary")
        if variable_dictionary_window.load_table(self.variable_dictionary):
            variable_dictionary_window.grab_set()
        else:
            variable_dictionary_window.destroy()

    def display_delta(self):
        delta_table_window = Table_Window.TableWindow(self.root, "Delta")
        if delta_table_window.load_table(self.delta):
            delta_table_window.grab_set()
        else:
            delta_table_window.destroy()

    def display_prepin(self, i, name):
        prepin_table_window = Table_Window.TableWindow(self.root, name)
        if prepin_table_window.load_table(self.prepin_files[i]):
            prepin_table_window.grab_set()
        else:
            prepin_table_window.destroy()

    def export_prepin(self, i, name):
        self.file_address = ""
        self.file_address = filedialog.asksaveasfilename(title="Export " + name + " to prepin.* file",
                                                         filetypes=([("prepin file (prepin.*)", "*prepin.*")]))
        if not(len(self.file_address)):
            return
        self.prepin_writer.set_dataset(data=self.prepin_files[i].copy())
        self.prepin_writer.write(file_name=self.file_address)

    def clear_all(self):
        self.clear_prepin_data()
        self.label_block_names_loaded.configure(text="No block dictionary loaded", foreground="red")
        self.label_variable_names_loaded.configure(text="No variable dictionary loaded", foreground="red")
        self.block_dictionary = []
        self.variable_dictionary = []

    def clear_prepin_data(self):
        # Removing menu options to save/display/export prepin files as csv
        for i in range(len(self.prepin_file_name_index)):
            self.save_prepin_submenu.delete(0)
            self.display_prepin_submenu.delete(0)
            self.export_prepin_submenu.delete(0)
        # Resetting the prepin combo boxes
        for combobox in self.comboboxes_prepin_selection:
            combobox.configure(values=[])
            combobox.set("No prepin.* files loaded")
        self.prepin_file_name_index = {}
        self.prepin_files = []
        self.delta = []

    def callback_clear_all(self):
        if messagebox.askyesno(title="Confirm data deletion", message="This operation will delete all loaded data, including dictionaries. Do you wish to proceed?"):
            self.clear_all()
        else:
            return

    def callback_clear_prepin_data(self):
        if messagebox.askyesno(title="Confirm data deletion", message="This operation will delete all data loaded from prepin.* files. Do you wish to proceed?"):
            self.clear_prepin_data()
        else:
            return

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
                    # If this is not the first line in this row, then this is not the variable name and so ignore
                    # subscripting
                    if len(row) == 0 and line[len(line) - 3] == ")":
                        for i in range(len(line)):
                            if line[i] == "(":
                                row.append(line[16:i])
                                row.append(line[i + 1:len(line) - 3])
                                break
                    # Non subscripted case
                    else:
                        row.append(line[16:len(line) - 2])
                        if len(row) == 1:
                            row.append("")

            line = fp.readline()
            line_number = line_number + 1

        fp.close()
        return rows

    def read_prepin_file(self, prepin_file_name):
        rows = [["NAME", "SUBSCRIPT", "DEFAULT_VALUE", "DESCRIPTION", "UNITS", "SET_VALUE", "REMARK"]]
        row = []

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
                            keys = list(self.unit_systems[self.unit_system_index[self.unit_system.get()]])
                            for j in range(1, len(generic_units) - 1):
                                if generic_units[j] in keys:
                                    units = units + self.unit_systems[self.unit_system_index[self.unit_system.get()]][generic_units[j]]
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
        return rows

    def calculate_delta(self):
        # Check if valid prepin files are currently selected in the prepin combo boxes
        keys = list(self.prepin_file_name_index)
        indices = []
        message = "Delta calculated from "
        for combobox in self.comboboxes_prepin_selection:
            if not(combobox.get() in keys):
                messagebox.showerror(title="Could not calculate delta", message="Invalid prepin file selection")
                return
            else:
                indices.append(self.prepin_file_name_index[combobox.get()])
                message = message + combobox.get() + " to "
        message = message[:len(message)-4]
        self.delta = [["NAME", "SUBSCRIPT", "DEFAULT_VALUE", "DESCRIPTION", "UNITS", "VALUE_1", "VALUE_2", "DELTA"]]
        # Temporary copy of prepin data as rows may be removed
        prepin_file = self.prepin_files[indices[1]].copy()

        # Step through each variable in prepin 1 and search for the same variable in prepin 2.
        for i in range(len(self.prepin_files[indices[0]])):
            match = False
            for j in range(len(prepin_file)):
                # Check for match in both name and subscript. Empty subscripts will satisfy the condition.
                if self.prepin_files[indices[0]][i][0].lower() == prepin_file[j][0].lower() and self.prepin_files[indices[0]][i][1] == prepin_file[j][1]:
                    match = True
                    # Check if the values of the variable are not equal.
                    if not (self.prepin_files[indices[0]][i][5] == prepin_file[j][5]):
                        row = self.prepin_files[indices[0]][i].copy()
                        # Removing the remark
                        if len(row) > 6:
                            row.pop()
                        row.append(prepin_file[j][5])
                        # Difference should be written for numeric variables, otherwise write "Non-numeric change".
                        try:
                            value_delta = float(row[6]) - float(row[5])
                            row.append(str(value_delta))
                        except ValueError:
                            row.append("Non-numeric change")
                        else:
                            row.append("Error")
                        self.delta.append(row)
                    # Remove the variable from prepin 2.
                    prepin_file.pop(j)
                    # Move on to the next variable in prepin 1.
                    break
            # If a match was not found, add the variable to delta as a deletion.
            if not match:
                row = self.prepin_files[indices[0]][i].copy()
                # Removing the remark
                if len(row) > 6:
                    row.pop()
                row.append("")
                row.append("REMOVED")
                self.delta.append(row)

        # After iterating through prepin 1 and deleting variable, subscript matches from prepin 2, the remaining prepin
        # 2 array only contains new variables added in prepin 2.
        for i in range(len(prepin_file)):
            row = prepin_file[i].copy()
            # Removing the remark
            if len(row) > 6:
                row.pop()
            row.append(row[5])
            row[5] = ""
            row.append("ADDED")
            self.delta.append(row)
        self.label_message.configure(text=message, foreground="black")

    def parameter_sweep(self):
        parameter_str = self.parameter_var.get()
        step_str = self.step_var.get()
        n_steps_str = self.n_steps_var.get()
        if not(len(parameter_str) and len(step_str)):
            messagebox.showerror(title="Missing Data",
                                 message="No parameters and/or no step values have been specified")
            return
        # Loading parameter sweeper with prepin data from first combobox
        combobox = self.comboboxes_prepin_selection[0]
        self.parameter_sweeper.set_origin(self.prepin_files[self.prepin_file_name_index[combobox.get()]].copy())
        self.parameter_sweeper.set_axes(parameter_str)
        self.parameter_sweeper.set_steps(step_str, n_steps_str)
        self.parameter_sweeper.parameter_sweep()

    def add_csv_file_extension(self):
        if not(self.file_address[len(self.file_address)-4:] == ".csv"):
            self.file_address = self.file_address + ".csv"
