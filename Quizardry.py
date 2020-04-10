# root file in the module/file hierarchy. Calls the load homepage function.
# created to enable 'back' button after selecting mcq vs true or false in the homepage

from tkinter import *
from homepage import open_homepage

root= Tk()
root.title("Quizardry")
root.geometry("700x600")
root.config(background="#ffffff")
root.resizable(0, 0)

open_homepage(root)


root.mainloop()