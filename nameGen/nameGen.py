#!/usr/bin/python3
import tkinter as tk
import json
import pygubu
from npc import *
from random import randint
import csv
import sys
import copy

class Application:
    def __init__(self, window, callbacks, title = None):
        self.builder = builder = pygubu.Builder()
        self.builder.add_from_file(window + '.ui')
        self.mainwindow = self.builder.get_object(window)
        if title:
            self.mainwindow.title(title)
        self.builder.connect_callbacks(callbacks)

    def run(self):
        self.mainwindow.mainloop()
    def quit(self):
        self.mainwindow.destroy()

class RootWindow(Application):
    def __init__(self):
        super().__init__('baseWindow', {
            'saveClicked' : self.save,
            'deleteClicked': self.deleteNPC,
            'editClicked': self.editNPC,
            'displayClicked': self.useNPC,
            'addNPCClicked': self.addNPC,
            'newNameClicked': self.makeName,
            'setGenderBox': self.setGenderBox
            }, "Fantasy Craft Name Generator")
        self.builder.get_object('genderBox').current(0)
        self.builder.get_object('speciesBox').current(0)
        self.genderBox = self.builder.get_object('genderBox')
        self.speciesBox = self.builder.get_object('speciesBox')
        self.nameBox = self.builder.get_object('nameBox')
        self.listBox = self.builder.get_object('listBox')
        self.children = {}
        for name,npc in npcs.items():
            self.listBox.insert("end", name)
            npcs[name] = NPC(name, npc)
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.onClose)

    def setGenderBox(self, event=None):
        if (self.speciesBox.get() in ['Rootwalker', 'Unborn', 'Drake']):
            self.genderBox.set('Both/Either/Other/None')
            self.genderBox.state(['disabled'])
        else:
            self.genderBox.state(['readonly'])

    def addNPC(self):
        name = self.nameBox.get()
        npcs[name] = NPC(name, {"gender" : self.genderBox.get(), "species" : self.speciesBox.get()})
        self.listBox.insert("end", name)

    def deleteNPC(self):
        for name in self.listBox.curselection():
            self.dl = self.listBox.curselection()
            messagebox = MessageWindow("Delete " + self.listBox.get(name) + "?", self.remove, None, "Delete?", "Delete", "Cancel")

    def remove(self):
        del npcs[self.listBox.get(self.dl)]
        self.listBox.delete(self.dl)
        self.dl = None

    def editNPC(self):
        for entry in self.listBox.curselection():
            name = self.listBox.get(entry)
            self.children[name] = EditWindow(npcs[name])
            self.children[name].run()
    def useNPC(self):
        for entry in self.listBox.curselection():
            name = self.listBox.get(entry)
            self.children[name] = DisplayWindow(npcs[name])
            self.children[name].run()

    def makeName(self):
        gender = self.genderBox.current()
        equation = formatTable[self.speciesBox.current()][d20()]
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
        self.nameBox.delete(0,'end')
        self.nameBox.insert(0,final)
    def save(self):
        with open("savedNPCs.json", "w") as saveFile:
            saveFile.write(json.dumps(npcs))

    def onClose(self):
        messagebox = MessageWindow("Do you wish to exit?", self.close, None, "Quit?", "Yes", "No")

    def close(self):
        for child,window in self.children.items():
            window.quit()
        self.quit()


class NPCWindow(Application):
    def __init__(self, npc, window, callbacks):
        super().__init__(window, callbacks, npc['name'])
        self.npc = copy.deepcopy(npc)
        self.builder.get_object('nameBox').insert("end",self.npc['name'])
        self.builder.get_object('textBox').insert("end", self.npc['text'])
        self.builder.get_object('genderBox').set(self.npc['gender'])
        self.builder.get_object('speciesBox').set(self.npc['species'])
        for trait,value in self.npc['traits'].items():
            self.builder.get_object(trait).set(value)


class EditWindow(NPCWindow):
    def __init__(self, npc):
        super().__init__(npc, 'editWindow', {
                'okayClicked': self.okay,
                'lockClicked': self.toggleLock,
                'cancelClicked': self.quit,
                'nameChanged': self.rename,
                'attributeChanged': self.updateAttributes
            })
        self.nameBox = self.builder.get_object('nameBox')
        self.textBox = self.builder.get_object('textBox')
        self.genderBox = self.builder.get_object('genderBox')
        self.speciesBox = self.builder.get_object('speciesBox')
        self.toggleLock()

    def okay(self, event = None):
        npcs[self.npc['name']]['gender'] = self.npc['gender']
        npcs[self.npc['name']]['species'] = self.npc['species']
        npcs[self.npc['name']]['text'] = self.npc['text']
        npcs[self.npc['name']]['traits'] = self.npc['traits']
        self.quit()

    def toggleLock(self, event = None):
        if self.speciesBox.state() == ("disabled",):
            self.speciesBox['state'] = 'readonly'
            self.genderBox['state'] ='readonly'
            self.nameBox['state'] = 'normal'
            self.builder.get_object('lockButton')['text'] = "Lock"
        else: 
            self.speciesBox['state'] = 'disabled'
            self.genderBox['state'] ='disabled'
            self.nameBox['state'] = 'disabled'
            self.builder.get_object('lockButton')['text'] = "Unlock"


    def rename(self, event = None):
        oldName = self.npc['name']
        newName = self.nameBox.get()
        if newName not in npcs:
            self.npc['name'] = newName
            npcs[newName] = self.npc
            del npcs[oldName]
        else:
            self.nameBox.delete(0,"end")
            self.nameBox.insert("end", oldName)

    def updateAttributes(self, event = None):
        self.npc['gender'] = self.genderBox.get()
        self.npc['species'] = self.speciesBox.get()
        for trait in self.npc['traits']:
            self.npc['traits'][trait] = self.builder.get_object(trait).get()
        self.npc['text'] = self.textBox.get("1.0","end").strip()

class DisplayWindow(NPCWindow):
    def __init__(self, npc):
        super().__init__(npc, 'displayWindow', {
                'threatUpdated' : updateDisplay
            })
        self.threatBox = self.builder.get_object('threatBox')
        threatBox.current(0)
        self.updateDisplay()
    def updateDisplay(self, event = None):
        pass

class MessageWindow(Application):
    def __init__(self, question, callbackYes, callbackNo, title = "Message Box", labelYes = 'Yes', labelNo = 'No'):
        super().__init__('messageWindow', {
                'yesClick' : self.yes,
                'noClick' : self.no,
            },title)
        self.callbackYes = callbackYes
        self.callbackNo = callbackNo
        self.builder.get_object('yesButton')['text']  = labelYes
        self.builder.get_object('noButton')['text'] = labelNo
        self.builder.get_object('message')['text'] = question
    def yes(self, event = None):
        self.quit()
        if self.callbackYes != None:
            self.callbackYes()
    def no(self, event = None):
        self.quit()
        if self.callbackNo != None:
            self.callbackNo()




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
npcs = {}
with open("savedNPCs.json") as saveFile:
    try:
        npcs = json.loads(saveFile.read())
    except:
        pass
def d20():
    return randint(0,19)

if __name__ == '__main__':
    app = RootWindow()
    app.run()
