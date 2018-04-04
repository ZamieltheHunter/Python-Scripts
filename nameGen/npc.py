from tkinter import *
import json

npcs = {}
with open("savedNPCs.json") as saveFile:
    npcs = json.loads(saveFile.read())

def save():
    with open("savedNPCs.json", "w") as saveFile:
        saveFile.write(json.dumps(npcs))

class NPC(dict):
    def __init__(self, name, data):
        dict.__init__(self)
        self.name = name
        self['gender'] = data['gender'] if 'gender' in data else "N"
        self['species'] = data['species'] if 'species' in data else "Undefined"
        self['text'] = data['text'] if 'text' in data else ""
        self.window = None
        self.frame = None
        self.entry = None
        self.genderBox = None
        self.speciesBox = None

    def closeWindow(self):
        self.window.destroy()
        self.window = None
        self.frame = None
        self.entry = None

    def saveChanges(self):
        npcs[self.name]['text'] = self.entry.get(1.0, END)
        npcs[self.name]['gender'] = self.genderBox.get()
        npcs[self.name]['species'] = self.speciesBox.get()

    def saveAndClose(self):
        self.saveChanges()
        self.closeWindow()

    def edit(self):
        self.window = Toplevel()
        self.window.title(self.name)
        self.frame = ttk.Frame(self.window, padding="3 3 12 12")
        self.frame.grid(column=0, row=0)
        self.entry = Text(self.window, width=30, height = 6)
        self.entry.insert(END, self['text'])
        self.genderBox = ttk.Combobox(self.frame, values = ['Male', 'Female', 'Either/Both/None'], state = ['readonly'])
        self.speciesBox = ttk.Combobox(self.frame, values = ['Drake', 'Dwarf', 'Elf', 'Giant', 'Goblin', 'Human', 'Ogre', 'Orc', 'Pech', 'Rootwalker', 'Saurian', 'Unborn'], state=['readonly'])
        self.speciesBox.grid(column = 0, row = 0)
        self.genderBox.grid(column = 0, row = 1)
        self.genderBox.set(self['gender'])
        self.speciesBox.set(self['species'])
        ttk.Button(self.frame, text="Save and Close", command=self.saveAndClose).grid(column = 0, row = 2)
        ttk.Button(self.frame, text="Cancel Edit", command=self.closeWindow).grid(column = 0, row = 3)
        self.entry.grid(column =2, row = 0)
    
    def delete(self):
        del npcs[self.name]
        self['name']= None
        self['gender'] = None
        self['species'] = None
        self['text'] = None
        if self.window:
            self.window.destroy()
        self.window = None
        self.frame = None
        self.entry = None
        self.genderBox = None
        self.speciesBox = None
