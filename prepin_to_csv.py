import csv
from numpy import *

# Convert a prepin file into a csv with columns NAME, SUBSCRIPT, DEFAULT_VALUE, DESCRIPTION, UNITS, SET_VALUE, REMARK.
# Access to a dictionary file is needed that links a name to its description, units and default value.
# Example of a variable definition with no subscript and a remark:
#    mu1=0.033, remark='viscosity',
# Example of a variable definition with a subscript but no remark:
#    scltit(1)='Cooling rate R',


def prepin_to_csv(prepin_file_name, block_name_dictionary, var_name_dictionary, csv_name, unit_system):

    # Array of block name entries
    block_names = []
    with open(block_name_dictionary, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row):
                block_names.append(row)

    # Array of variable name entries
    var_names = []
    with open(var_name_dictionary, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row):
                var_names.append(row)

    rows = [["NAME", "SUBSCRIPT", "DEFAULT_VALUE", "DESCRIPTION", "UNITS", "SET_VALUE", "REMARK"]]
    row = []

    fp = open(prepin_file_name, "r")

    line = " "

    while line:
        line = fp.readline()

        # An ampersand as the second character indicates the line contains a block name.
        if len(line) > 2 and line[1] == "&":
            # Searching the dictionary.
            for i in range(len(block_names)):
                if line[2:len(line)-1].lower() == block_names[i][0].lower():
                    row = [block_names[i][0], "BLOCK", "BLOCK", block_names[i][2], "BLOCK", "BLOCK", "BLOCK"]
                    break
            # Case where dictionary entry is missing.
            if len(row) == 0:
                row = [line[2:len(line)-1], "BLOCK", "BLOCK", "MISSING DESCRIPTION", "BLOCK", "BLOCK", "BLOCK"]

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
                            subscript = line[i+1:j]
                            break
                if line[i] == "=":
                    if not(len(var_name)):
                        var_name = line[4:i]
                    # Variable lines always end with ",\n".
                    for j in range(i, len(line)):
                        # End of the value indicated by a comma. After the comma we may have a remark.
                        if line[j] == ",":
                            value = line[i+1:j]
                            remark = line[j+1:len(line)-2]
                            break
                    break
            # Removing "remark=" from the remark.
            for i in range(len(remark)):
                if remark[i] == "=":
                    remark = remark[i+1:]
                    break
            # Remarks are not considered variables.
            if var_name == "remark":
                continue
            row = [var_name, "MISSING SUBSCRIPT DESCRIPTION", "MISSING DEFAULT VALUE", "MISSING DESCRIPTION",
                   "MISSING UNITS"]
            # Searching the dictionary.
            for i in range(len(var_names)):
                if var_name.lower() == var_names[i][0].lower():
                    # Case where a generic expression is given for the units.
                    if len(var_names[i]) > 4 and var_names[i][4][0] == "[":
                        generic_units = var_names[i][4].replace("\ :sup:", "^")
                        units = ""
                        keys = list(unit_system)
                        for j in range(1, len(generic_units)-1):
                            if generic_units[j] in keys:
                                units = units + unit_system[generic_units[j]]
                            # Remove backticks
                            elif generic_units[j] == "`":
                                continue
                            else:
                                units = units + generic_units[j]
                        row = var_names[i][:4].copy()
                        row.append(units)
                    else:
                        row = var_names[i].copy()
                    break
            row[1] = subscript
            row.append(value)
            row.append(remark)

        if len(row):
            rows.append(row)
            row = []

    fp.close()

    with open(csv_name, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)
