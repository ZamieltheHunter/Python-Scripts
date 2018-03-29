#!/usr/bin/python3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import json
import csv
import savedNPCs as NPCs
from random import randint
import sys

npcs = NPCs.npcs
edits = {}

def setGenderBox(value):
    if (speciesBox.get() in ['Rootwalker', 'Unborn', 'Drake']):
        genderBox.set('Either/Both/None')
        genderBox.state(['disabled'])
    else:
        genderBox.state(['!disabled'])

def d20():
    return randint(0,19)

def onClose():
    if messagebox.askokcancel("Quit", "Do you wish to exit?"):
        for window in edits:
            edits[window]["root"].destroy()
        root.destroy()

def save():
    with open("savedNPCs.py", "w") as saveFile:
        saveFile.write("npcs =" + json.dumps(npcs))

def exitNPCEdit(npc):
    edits[npc]["root"].destroy()

def saveAndExitEdit(npc):
    npcs[npc]["text"] = edits[npc]["entry"].get(0, END)
    exitNPCEdit(npc)

def addNPC():
    npcs[nameBox.get()] = {"text":""}
    listBox.insert(END, nameBox.get())

def deleteNPC():
    for npc in listBox.curselection():
        del npcs[listBox.get(npc)]
    listBox.delete(0, END)
    for npc in npcs:
        listBox.insert(END, npc)

def editNPC():
    for entry in listBox.curselection():
        npc = listBox.get(entry)
        edits[npc] = {}
        cur = edits[npc]
        cur["root"] = Toplevel()
        cur["frame"] = ttk.Frame(cur["root"], padding="3 3 12 12")
        cur["frame"].grid(column=0,row=0, sticky=(N, W, E, S))
        cur["frame"].columnconfigure(0,weight=1)
        cur["frame"].rowconfigure(0,weight=1)
        cur["entry"] = Text(cur["frame"])
        cur["entry"].insert(END, npcs[npc]["text"])
        ttk.Button(cur["frame"],text="Save & Exit", command= lambda:saveAndExitEdit(npc)).grid(column = 0, row = 0)
        ttk.Button(cur["frame"],text="Cancel", command= lambda: exitNPCEdit(npc)).grid(column=0, row=1)
        cur["entry"].grid(column=1, row = 0)

def makeName():
    gender = genderBox.current()
    equation = formatTable[speciesBox.current()][d20()]
    final = ""
    first = 0
    for symbol in equation:
        if("A" <= symbol < "P" or symbol == "X"):
            sym = ord(symbol) - 65
            part = ''
            if(sym < 10):
                part = nameTable[ord(symbol) - 65][d20()]
            elif(sym == 11 or sym == 12):
                if(gender == 2):
                    gender = randint(0,1)
                part = nameTable[sym][d20()].split("/")[gender];
            elif(symbol == "X"):
                part = str(randint(0,10000))
            else:
                part = nameTable[sym][d20()].split("/")[first]
            
            if(first != 0):
                final += part.lower()
            else :
                final += part
        else:
            final += symbol

        if(symbol == " "):
            first = 0
        else:
            first = 1
    nameBox.delete(0,'end')
    nameBox.insert(0,final)

if getattr(sys, 'frozen', False):
    formatFile = sys._MEIPASS + "/format.csv"
    nameFile = sys._MEIPASS + "/sorted.csv"
else:
    formatFile = "format.csv"
    nameFile = "sorted.csv"
with open(nameFile, "r") as table:
    reader = csv.reader(table)
    nameTable = [[c for c in r] for r in reader]
with open(formatFile, "r") as table:
    reader = csv.reader(table)
    formatTable =[[c for c in r] for r in reader]

root = Tk()
root.title("Fantasy Craft Name Generator")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0,row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0,weight=1)
mainframe.rowconfigure(0,weight=1)
generatedName = ''
speciesBox = ttk.Combobox(mainframe)
speciesBox['values'] = ('Drake', 'Dwarf', 'Elf', 'Giant', 'Goblin', 'Human', 'Ogre', 'Orc', 'Pech', 'Rootwalker', 'Saurian', 'Unborn')
speciesBox.state(['readonly'])
speciesBox.current(0)
speciesBox.bind("<<ComboboxSelected>>", setGenderBox)
speciesBox.grid(column=1, row=0, sticky=E)
genderBox = ttk.Combobox(mainframe)
genderBox['values'] = ('Male','Female','Either/Both/None')
genderBox.state(['readonly'])
genderBox.current(0)
genderBox.grid(column=1, row=1, sticky=E)

nameBox = ttk.Entry(mainframe)
nameBox.grid(column=1,row=2, sticky=E)

listBox = Listbox(root)
listBox.grid(column=3, row=0)
for name in npcs.keys():
    listBox.insert(END, name)

ttk.Button(mainframe, text="Save", command=save).grid(column=2, row=0)
ttk.Button(mainframe, text="Add NPC", command=addNPC).grid(column=2, row=1)
ttk.Button(mainframe, text="New Name", command=makeName).grid(column=2,row=4)
ttk.Button(mainframe, text="Delete", command=deleteNPC).grid(column=2,row=2)
ttk.Button(mainframe, text="Edit", command=editNPC).grid(column=2, row =3)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
root.bind('<Return>',makeName)
root.protocol("WM_DELETE_WINDOW", onClose)

root.mainloop()
