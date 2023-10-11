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
    # Reading each csv file into 2 dimensional arrays.
    prepin_1 = []
    with open(prepin_csv_1, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row):
                prepin_1.append(row)

    prepin_2 = []
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
                if not(prepin_1[i][5] == prepin_2[i][5]):
                    # TODO Check if the variable is numeric including the decimal point and scientific notation.
                    row = prepin_1[i].copy()
                    row.append(prepin_2[j][5])
                    row.append("VAL_CHANGE")
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
