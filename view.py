import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.filedialog import askdirectory
from tkinter import scrolledtext
import os

SCROLL_X = 30
MAX = 100

def batchProcess():
    return

def startCheck():
    return

def setDefaultPaths():
    return


def getDirPath(entry):
    return

def clearLogs():
    return

def _quit():
    win.destroy()
    win.quit()


win = tk.Tk()
win.title("EyeCare - 1.0")
win.resizable(0,0)
win.configure(padx=10,pady=10)

#creating tabs for home and settings
tabControl = ttk.Notebook(win)

home = ttk.Frame(tabControl)
tabControl.add(home,text="Single Mode")
tabControl.pack(expand=1,fill="both")

batch = ttk.Frame(tabControl)
tabControl.add(batch,text="Batch Mode")
tabControl.pack(expand=1,fill="both")

settings = ttk.Frame(tabControl)
tabControl.add(settings,text="Settings")
tabControl.pack(expand=1,fill="both")
#tab creation END

#Pre and Post directories frame
dirInput = ttk.LabelFrame(home,text="Directories")
dirInput.grid(column=0,row=0,padx=10,pady=5)

source = tk.StringVar()
sourceInput = tk.Entry(dirInput,width=SCROLL_X,textvariable=source)
sourceInput.grid(column=1,row=0,stick=tk.E)
sourceButton = ttk.Button(dirInput,text="Browse Post: ",command=lambda:getDirPath(sourceInput))
sourceButton.grid(column=0,row=0,sticky=tk.W)

dest = tk.StringVar()
destInput = tk.Entry(dirInput,width=SCROLL_X,textvariable=dest)
destInput.grid(column=1,row=1,stick=tk.E)
destButton = ttk.Button(dirInput,text="Browse Pre: ",command=lambda:getDirPath(destInput))
destButton.grid(column=0,row=1,sticky=tk.W)

for child in dirInput.winfo_children():
    child.grid_configure(padx=6,pady=6)

setDefaultPaths()
#------------end------------

#configuration options

configFrame = ttk.LabelFrame(home,text="Configuration Option")
configFrame.grid(column=0,row=1,stick=tk.W,padx=10,pady=5)

regenerateOption =  tk.IntVar()
check1 = tk.Checkbutton(configFrame,text="Regenerate Image",variable=regenerateOption)
check1.grid(column=0,row=0,sticky=tk.W)

reportGeneration =  tk.IntVar()
check2 = tk.Checkbutton(configFrame,text="Generate Report",variable=reportGeneration)
check2.grid(column=1,row=0,sticky=tk.W)

batchMode =  tk.IntVar()
check3 = tk.Checkbutton(configFrame,text="Batch Mode",variable=batchMode)
check3.grid(column=0,row=1,sticky=tk.W)


for child in configFrame.winfo_children():
    child.grid_configure(padx=6,pady=6)

#-------end

#log area

logarea = scrolledtext.ScrolledText(home,width=50,height=15,wrap=tk.WORD)
logarea.grid(column=0,row=2,sticky='WE')

progressBar = ttk.Progressbar(home,orient="horizontal",mode="determinate",length=390)
progressBar.grid(column=0,row=3,columnspan=1)
progressBar.grid_columnconfigure(0,weight=1)


#----end----

#controls

controlFrame = ttk.LabelFrame(home,borderwidth=0)
controlFrame.grid(column=0,row=4,padx=10,pady=5,sticky=tk.E)

startCheck = ttk.Button(controlFrame,text="Start",command=startCheck)
startCheck.grid(column=0,row=0,sticky=tk.E)
batchCheck = ttk.Button(controlFrame,text="Batch Start",command=batchProcess)
batchCheck.grid(column=1,row=0,sticky=tk.E)
clearlogs = ttk.Button(controlFrame,text="Clear",command=clearLogs)
clearlogs.grid(column=2,row=0,sticky=tk.E)
quit = ttk.Button(controlFrame,text="Quit",command=_quit)
quit.grid(column=3,row=0,sticky=tk.W)

win.mainloop()
