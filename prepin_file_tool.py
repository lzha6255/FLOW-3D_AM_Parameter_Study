import dictionary

from tkinter import *
from tkinter import filedialog


class PrepinFileTool:
    def __init__(self):
        self.prepin_variable_arrays = []
        self.variable_dictionary = []
        self.block_dictionary = []
        self.file_address = ""
        self.filenames = []

        self.root = Tk()
        self.root.title("FLOW-3D prepin file tool")
        self.root.geometry("1000x500")

        self.button_select_file = Button(self.root, text="Select file", command=self.select_file)
        self.button_exit = Button(self.root, text="Exit", command=exit)

        self.label_file_opened = Label(self.root, text="Last file opened: ")

        self.button_select_file.grid(row=0, column=0)
        self.label_file_opened.grid(row=1, column=0)
        self.button_exit.grid(row=2, column=0)

    def start(self):
        self.root.mainloop()

    def select_file(self):
        self.file_address = filedialog.askopenfilename(initialdir="\\", title="Select a file",
                                                       filetypes=(("text files", "*.txt*"), ("all files", "*.*")))
        self.label_file_opened.configure(text="Last file opened: "+self.file_address)
        print(self.file_address)
