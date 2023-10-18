from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox


class TableWindow(Toplevel):
    def __init__(self, parent, title):
        super().__init__(parent)

        self.geometry("500x500")
        self.title(title)

        self.tree = Treeview(self, columns=[], show="headings")
        self.tree.pack()

    # Expects data to be a 2-D array where the first row is a header row.
    def load_table(self, data):
        if not(len(data)):
            messagebox.showerror(title="Data not loaded",
                                 message="Please check if the dataset you are trying to load exists")
            # If no data has been loaded into the window, return 0
            if not(len(self.tree["columns"])):
                return 0
            return 1
        self.tree.configure(columns=data[0])
        for heading in data[0]:
            self.tree.heading(heading, text=heading)
        for row in data[1:]:
            self.tree.insert("", END, values=row)
        return 1
