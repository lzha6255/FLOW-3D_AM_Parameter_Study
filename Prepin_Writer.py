# Checks if the file address is of the form prepin.*
# If it is not, then returns an address in the form prepin.*
# Otherwise returns the address that was passed in.
def prepin_file_address_verifier(file_address):
    for i in range(len(file_address)-1, 0, -1):
        if file_address[i] == "/":
            # Case where the prepin.* prefix is missing
            if len(file_address) - i < 8 or not(file_address[i+1:i+8] == "prepin."):
                return file_address[:i+1] + "prepin." + file_address[i+1:]
            else:
                return file_address


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

        file_address = prepin_file_address_verifier(file_name)
        print(file_address)

        fp = open(file_address, "w")

        first_block = True
        for i in range(1, len(self.prepin_data)):
            # Enforce that rows of prepin data are at least 6 long
            if len(self.prepin_data[i]) < 7:
                fp.close()
                return -1
            # Writing Blocks
            if self.prepin_data[i][1] == "BLOCK":
                if not(first_block):
                    fp.writelines([" /\n", "\n"])
                fp.write(" &" + self.prepin_data[i][0].lower() + "\n")
                first_block = False
            # Writing Parameters
            else:
                line = "    " + self.prepin_data[i][0].lower()
                # Adding subscript if it exists
                if len(self.prepin_data[i][1]):
                    line = line + "(" + self.prepin_data[i][1] + ")"
                line = line + "=" + self.prepin_data[i][5] + ","
                # Adding remark if it exists
                if len(self.prepin_data[i][6]):
                    line = line + " remark='" + self.prepin_data[i][6] + "',"
                line = line + "\n"
                fp.write(line)

        fp.close()
