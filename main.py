import dictionary
import prepin_to_csv
import delta
import prepin_file_tool


if __name__ == '__main__':
    cgs_kelvin = {"M": "g", "L": "cm", "T": "K", "t": "s", "Q": "scoul"}

    block_name_file = "block_names.txt"
    variable_name_file = "input-variable-summary-units.rst.txt"
    block_name_csv = "block_names.csv"
    variable_name_csv = "variable_names.csv"
    block_name_header = ["NAMELIST", "", "DESCRIPTION", "REQUIRED"]
    variable_name_header = ["NAME", "SUBSCRIPT", "DEFAULT_VALUE", "DESCRIPTION", "DIMENSIONS"]

    dictionary.write_dictionary(block_name_file, block_name_csv, block_name_header)
    dictionary.write_dictionary(variable_name_file, variable_name_csv, variable_name_header)

    prepin_file_name = "prepin.Solidification"
    prepin_2_fname = "prepin.ship_propeller_1"

    prepin_to_csv.prepin_to_csv(prepin_file_name, block_name_csv, variable_name_csv, cgs_kelvin)
    delta.write_delta(prepin_file_name, prepin_2_fname)

    prepin_tool = prepin_file_tool.PrepinFileTool()
    prepin_tool.start()
