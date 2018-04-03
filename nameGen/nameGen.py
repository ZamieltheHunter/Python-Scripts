#!/usr/bin/python3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from npc import *
from random import randint
import csv
import sys

names = list(npcs)

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
        root.destroy()

def addNPC():
    name = nameBox.get()
    names.append(name)
    npcs[name] = NPC(name, {"gender" : genderBox.get(), "species" : speciesBox.get()})
    listBox.insert(END, name)

def deleteNPC():
    for name in listBox.curselection():
        if messagebox.askokcancel("Confirm Delete", "Delete " + listBox.get(name) + "?"):
            npcs[listBox.get(name)].delete()

    listBox.delete(0, END)
    for npc in npcs:
        listBox.insert(END, npc)

def editNPC():
    for entry in listBox.curselection():
        name = listBox.get(entry)
        npcs[name].edit()

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
for name in names:
    listBox.insert(END, name)
    npcs[name] = NPC(name, npcs[name])

ttk.Button(mainframe, text="Save", command=save).grid(column=2, row=0)
ttk.Button(mainframe, text="Add NPC", command=addNPC).grid(column=2, row=1)
ttk.Button(mainframe, text="New Name", command=makeName).grid(column=2,row=4)
ttk.Button(mainframe, text="Delete", command=deleteNPC).grid(column=2,row=2)
ttk.Button(mainframe, text="Edit", command=editNPC).grid(column=2, row =3)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
root.bind('<Return>',makeName)
root.protocol("WM_DELETE_WINDOW", onClose)

root.mainloop()
