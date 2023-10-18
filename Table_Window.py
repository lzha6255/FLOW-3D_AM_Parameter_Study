from tkinter import *
from tkinter.ttk import *


class TableWindow(Toplevel):
    def __init__(self, parent, title):
        super().__init__(parent)

        self.geometry("500x500")
        self.title(title)

        self.tree = Treeview(self, columns=[], show="headings")
        self.tree.pack()

    # Expects data to be a 2-D array where the first row is a header row.
    def load_table(self, data):
        self.tree.configure(columns=data[0])
        for heading in data[0]:
            self.tree.heading(heading, text=heading)
        for row in data[1:]:
            self.tree.insert("", END, values=row)
