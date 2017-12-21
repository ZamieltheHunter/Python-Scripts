#!/usr/bin/python3
from tkinter import *
from tkinter import ttk
import csv
from random import randint

speciesMap = {'Drake' : 0, 'Dwarf' : 1, 'Elf' : 2, 'Giant' : 3, 'Goblin' : 4, 'Human' : 5, 'Ogre' : 6, 'Orc' : 7, 'Pech' : 8, 'Rootwalker' : 9, 'Saurian' : 10, 'Unborn' : 11}
def d20():
    return randint(0,19)
def makeName():
    gender = genderBox.current()
    equation = formatTable[speciesBox.current()][d20()]
    final = ""
    first = 0
    for symbol in equation:
        if("A" <= symbol < "P"):
            sym = ord(symbol) - 65
            part = ''
            if(sym < 10):
                part = nameTable[ord(symbol) - 65][d20()]
            elif(sym == 11 or sym == 12):
                part = nameTable[sym][d20()].split("/")[gender];
            elif(symbol == "X"):
                part = str(d20())
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
with open("sorted.csv", "r") as table:
    reader = csv.reader(table)
    nameTable = [[c for c in r] for r in reader]
with open("format.csv", "r") as table:
    reader = csv.reader(table)
    formatTable =[[c for c in r] for r in reader]

#makeName(1, formatTable[species][form])

root = Tk()
root.title("Fantasy Craft Name Generator")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0,row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0,weight=1)
mainframe.rowconfigure(0,weight=1)
selectedGender = ''
selectedSpecies = ''
generatedName = ''
speciesBox = ttk.Combobox(mainframe,textvariable=selectedSpecies)
speciesBox['values'] = ('Drake', 'Dwarf', 'Elf', 'Giant', 'Goblin', 'Human', 'Ogre', 'Orc', 'Pech', 'Rootwalker', 'Saurian', 'Unborn')
speciesBox.state(['readonly'])
speciesBox.current(0)
genderBox = ttk.Combobox(mainframe,textvariable=selectedGender)
genderBox['values'] = ('Male','Female')
genderBox.state(['readonly'])
genderBox.current(0)

nameBox = ttk.Entry(mainframe, textvariable=generatedName)

generate = ttk.Button(mainframe, text="New Name", command=makeName).grid(column=3,row=3,sticky=W)
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
root.bind('<Return>',makeName)

root.mainloop()
