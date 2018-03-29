from tkinter import *
import json
import savedNPCs as NPCs

class NPC():
    def __init__(self, name, race, gender, text=""):
        self.name = name
        self.gender = gender
        self.race = race
        self.text = text
        self.window = None
        self.frame = None
        self.entry = None

    def saveChanges():
        npcs[self.name]["text"] = self.entry.get(0, END)

    def onClose():
        if messagebox.askokcancel("Quit", "Do you wish to save your changes?")
            self.saveChanges()
        self.window.destroy()
        self.window = None
        self.frame = None
        self.entry = None

    def spawnWindow():
        self.window = Toplevel
        self.window.title(self.name)
        self.frame = ttk.Frame(column=0, row=0)
        self.frame.grid(column=3, row=3)
        self.entry = Text(self.window)
        self.window.protocol("WM_DELETE_WINDOW", self.onClose)

    def edit():
        self.spawnWindow()
        self.window
