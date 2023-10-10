import csv
# Reads in the parameter code, description, units and default value and creates a dictionary in the form of a
# csv file.

# Each dictionary entry is given on multiple lines, and always starts with a "*".
# For block names, the format is:
#   *  - NAMELIST
#      - DESCRIPTION
#      - REQUIRED


def write_dictionary(file_name, csv_name, fields, header):
    fp = open(file_name, "r")

    line = fp.readline()
    line_number = 1
    rows = []
    row = header

    while line:
        # "*" indicates the start of an entry, so the column number is now tracked.
        if len(line) > 7 and line[3:6] == "* -":
            if not(row[0] == "NAME" or row[0] == "NAMELIST") or len(rows) == 0:
                rows.append(row)
                print("Appending row at line number " + str(line_number))
            row = []

        # Each field in a dictionary entry is preceded by a hyphen.
        if len(line) > 6 and line[5:7] == "- ":
            if len(line) < 16 or not(line[7:15] == ":envvar:"):
                row.append(line[7:len(line)-1])
            # Variable names are preceded by ":envvar:" and surrounded by backticks.
            else:
                # Sometimes the variable name may have a subscript in brackets
                if line[len(line)-3] == ")":
                    for i in range(len(line)):
                        if line[i] == "(":
                            row.append(line[16:i])
                            row.append(line[i+1:len(line)-3])
                            break
                # Non subscripted case
                else:
                    row.append(line[16:len(line)-2])
                    row.append("")

        line = fp.readline()
        line_number = line_number + 1
    
    fp.close()

    with open(csv_name, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)
    print("Lines read: " + str(line_number))
