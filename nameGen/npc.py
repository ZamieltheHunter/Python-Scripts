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

    def closeWindow(self):
        self.window.destroy()
        self.window = None
        self.frame = None
        self.entry = None

    def saveChanges(self):
        npcs[self.name]['text'] = self.entry.get(1.0, END)

    def saveAndClose(self):
        self.saveChanges()
        self.closeWindow()

    def edit(self):
        self.window = Toplevel()
        self.window.title(self.name)
        self.frame = ttk.Frame(self.window, padding="3 3 12 12")
        self.frame.grid(column=3, row=3)
        self.entry = Text(self.window)
        self.entry.insert(END, self['text'])
        self.entry.grid(column = 0, row = 0)
        ttk.Button(self.frame, text="Save and Close", command=self.saveAndClose).grid(column = 3, row = 3)
        ttk.Button(self.frame, text="Cancel Edit", command=self.closeWindow).grid(column = 3, row = 2)
    
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
