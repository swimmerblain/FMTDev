from tkinter import *
from subprocess import call

pyarm = 'armfbk.py'
def callarm(): call(['python3', '-i', pyarm])

root = Tk()
Button(root, text='Run', command=callarm).pack()
root.mainloop()
