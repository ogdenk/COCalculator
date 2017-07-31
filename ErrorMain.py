import tkinter
from tkinter import messagebox
import time


def ErrorStart(errormsg):
    root = tkinter.Tk()
    root.withdraw()
    #messagebox.showerror("Error", errormsg)
    messagebox.showwarning("Warning",errormsg)
    #messagebox.showinfo("Info","Info Message")
