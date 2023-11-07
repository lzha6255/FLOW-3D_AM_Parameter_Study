

class PrepinWriter:
    def __init__(self):
        self.prepin_data = []       # The dataset

    def set_dataset(self, data):
        self.prepin_data = data

    # Writes a single prepin file. Return values:
    # 1     = OK
    # 0     = Dataset missing
    # -1    = Incomplete dataset with a row of length < 6
    def write(self, file_name):
        if not(len(self.prepin_data)):
            return 0

        fp = open(file_name, "w")

        first_block = True
        for i in range(len(self.prepin_data)):
            # Enforce that rows of prepin data are at least 6 long
            if len(self.prepin_data[i]) < 7:
                return -1
            # Writing Blocks
            if self.prepin_data[i][1] == "BLOCK":
                if not(first_block):
                    fp.writelines([" /", ""])
                fp.write(" &" + self.prepin_data[i][0].lower())
                first_block = False
            # Writing Parameters
            else:
                line = "\t" + self.prepin_data[i][0].lower()
                # Adding subscript if it exists
                if len(self.prepin_data[i][1]):
                    line = line + "(" + self.prepin_data[i][1] + ")"
                line = line + "=" + self.prepin_data[i][5] + ","
                # Adding remark if it exists
                if len(self.prepin_data[i][6]):
                    line = line + " remark='" + self.prepin_data[i][6] + "',"
                fp.write(line)

        fp.close()
