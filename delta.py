import csv

# Reads in two prepin files, both processed into csv format. Compares the values between the two files and outputs the
# change in value as another csv file referred to as a delta file.
# The columns of the delta file are as follows:
# NAME, SUBSCRIPT, DEFAULT_VALUE, DESCRIPTION, UNITS, VALUE_1, VALUE_2, DELTA
# The delta file does not include rows where DELTA = 0 or None.
# In the case where a variable is present in one file but not in the other:
# DELTA = "+" where VALUE_1 is missing.
# DELTA = "-" where VALUE_2 is missing.

def write_delta(prepin_csv_1, prepin_csv_2):

    delta_csv_fname = "delta_files\\delta_" + prepin_csv_1 + "_" + prepin_csv_2 + ".csv"

    # Reading each csv file into 2 dimensional arrays.
    prepin_1 = []
    prepin_csv_1 = "prepin_csv_files\\" + prepin_csv_1 + ".csv"
    with open(prepin_csv_1, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row):
                prepin_1.append(row)

    prepin_2 = []
    prepin_csv_2 = "prepin_csv_files\\" + prepin_csv_2 + ".csv"
    with open(prepin_csv_2, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row):
                prepin_2.append(row)

    delta = [["NAME", "SUBSCRIPT", "DEFAULT_VALUE", "DESCRIPTION", "UNITS", "VALUE_1", "VALUE_2", "DELTA"]]

    # Step through each variable in prepin 1 and search for the same variable in prepin 2.
    for i in range(len(prepin_1)):
        match = False
        for j in range(len(prepin_2)):
            # Check for match in both name and subscript. Empty subscripts will satisfy the condition.
            if prepin_1[i][0].lower() == prepin_2[j][0].lower() and prepin_1[i][1] == prepin_2[j][1]:
                match = True
                # Check if the values of the variable are not equal.
                if not(prepin_1[i][5] == prepin_2[j][5]):
                    row = prepin_1[i].copy()
                    row.append(prepin_2[j][5])
                    # Difference should be written for numeric variables, otherwise write "Non-numeric change".
                    try:
                        value_delta = float(row[6]) - float(row[5])
                        row.append(str(value_delta))
                    except ValueError:
                        row.append("Non-numeric change")
                    else:
                        row.append("Error")
                    delta.append(row)
                # Remove the variable from prepin 2.
                prepin_2.pop(j)
                # Move on to the next variable in prepin 1.
                break
        # If a match was not found, add the variable to delta as a deletion.
        if not match:
            row = prepin_1[i].copy()
            row.append("")
            row.append("-")
            delta.append(row)

    # After iterating through prepin 1 and deleting variable, subscript matches from prepin 2, the remaining prepin 2
    # array only contains new variables added in prepin 2.
    for i in range(len(prepin_2)):
        row = prepin_2[i].copy()
        row.append(row[5])
        row[5] = ""
        row.append("+")
        delta.append(row)

    with open(delta_csv_fname, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(delta)
