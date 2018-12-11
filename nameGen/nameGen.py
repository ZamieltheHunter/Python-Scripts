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
            'openClicked': self.openNPC,
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

    def openNPC(self):
        for entry in self.listBox.curselection():
            name = self.listBox.get(entry)
            self.children[name] = NPCWindow(npcs[name])
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
    def __init__(self, npc):
        super().__init__("npcWindow",{
            'okayClicked': self.okay,
            'toggleEdit': self.toggleEdit,
            'cancelClicked': self.quit,
            'nameChanged': self.rename,
            'attributeChanged': self.updateAttributes,
            'threatUpdated' : self.updateDisplay
        }, npc['name'])
        self.npc = copy.deepcopy(npc)
        uiList = ['threatLabel', 'nameBox', 'textBox', 'genderBox', 'speciesBox', 'toggleButton',
                'threatBox', 'reachBox', 'sizeBox', 'speedBox', 'typeBox']
        for element in uiList:
            self[element] = self.builder.get_object(element)
        self.nameBox.insert("end", self.npc['name'])
        self.textBox.insert("end", self.npc['text'])
        self.genderBox.set(self.npc['gender'])
        self.speciesBox.set(self.npc['species'])
        self.reachBox.set(self.npc['reach'])
        self.sizeBox.set(self.npc['size'])
        self.speedBox.set(self.npc['speed'])
        self.typeBox.set(self.npc['type'])
        self.threatBox.current(0)
        self.builder.get_object('spaceLabel1').lower()
        self.builder.get_object('spaceLabel2').lower()
        for trait in self.npc['traits']:
            try:
                self.builder.get_object(trait).grid_remove()
            except:
                print("%sEntry not found" % trait)
        self.updateDisplay()
        self.toggleEdit()

    def okay(self, event = None):
        npcs[self.npc['name']]['gender'] = self.npc['gender']
        npcs[self.npc['name']]['species'] = self.npc['species']
        npcs[self.npc['name']]['text'] = self.npc['text']
        npcs[self.npc['name']]['traits'] = self.npc['traits']
        self.quit()

    def toggleEdit(self, event = None):
        if self.speciesBox.state() == ("disabled",):
            self.speciesBox['state'] = 'readonly'
            self.genderBox['state'] ='readonly'
            self.nameBox['state'] = 'normal'
            self.sizeBox['state'] = 'normal'
            self.speedBox['state'] = 'normal'
            for trait in self.npc['traits']:
                try:
                    self.builder.get_object(trait).grid()
                    self.builder.get_object("%sEntry" % trait).grid_remove()
                except:
                    print("%sEntry not found" % trait)
            for attribute in self.npc['attributes']:
                self.builder.get_object('%sEntry' % attribute)['state'] = 'normal'
            self.threatLabel.lower()
            self.threatBox.grid_remove()
            self.toggleButton['text'] = "Display"
            self.showAttributes()
        else: 
            self.speciesBox['state'] = 'disabled'
            self.genderBox['state'] ='disabled'
            self.nameBox['state'] = 'disabled'
            for trait in self.npc['traits']:
                try:
                    self.builder.get_object("%sEntry" % trait).grid()
                    self.builder.get_object(trait).grid_remove()
                except:
                    print("%sEntry not found" % trait)
            for attribute in self.npc['attributes']:
                self.builder.get_object("%sEntry" % attribute)['state'] = 'readonly'
            self.threatLabel.lift()
            self.threatBox.grid()
            self.threatBox.current(0)
            self.toggleButton['text'] = "Edit"
            self.updateDisplay()

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
        exp = 0
        self.npc['gender'] = self.genderBox.get()
        self.npc['species'] = self.speciesBox.get()
        self.npc['speed'] = self.speedBox.get()
        exp += Math.max([0, (int(self.npc['speed']) - 30) / 10])
        self.npc['size'] = self.sizeBox.get()

        for attribute in self.npc['attributes']:
            self.npc['attributes'] = self.builder.get_object(attribute).get()
            exp += Math.max([0, int(self.npc['attributes'][attribute]) - 10])
        for trait in self.npc['traits']:
            self.npc['traits'][trait] = self.builder.get_object(trait).get()
            exp += int(self.npc['traits'][trait])
        self.npc['text'] = self.textBox.get("1.0","end").strip()
        self.npc['experience'] = exp

    def updateDisplay(self, event = None):
        mods = {}
        finTraits = {}
        for trait, value in self.npc['traits'].items():
            box = self.builder.get_object("%sEntry" % trait)
            table = int(traitTables[trait])
            traitValue = int(value) - 1
            threat = int(self.threatBox.get())
            box['state'] = "normal"
            box.delete(0,"end")
            finTraits[trait] = 0 if traitValue == -1 else int(traitTables['tables'][table][traitValue][threat])
            box.insert("end", "%d" % finTraits[trait])
            box['state'] = "readonly"
        for attribute, value in self.npc['attributes'].items():
            box = self.builder.get_object('%sEntry' % attribute)
            box['state'] = "normal"
            box.delete(0, "end")
            mods[attribute] = (int(value) - 10) / 2
            box.insert("end", "%d" % mods[attribute])
            box['state'] = "readonly"

        self.builder.get_object('initMod').text("%d" % finTraits['init'] + mods['dex'])
        self.builder.get_object('healthSave').text("%d" % finTraits['health'] + mods['con'])
        self.builder.get_object('melee').text("%d" % finTraits['attack'].text()) + mods['str'])
        self.builder.get_object('ranged').text("%d" % finTraits['attack'] + mods['dex'])
        self.builder.get_object('finDefense').text("%d" % finTraits['defense'] + mods['dex'])
        self.builder.get_object('fortitude').text("%d" % finTraits['resilience'] + mods['con'])
        self.builder.get_object('reflex').text("%d" % finTraits['resilience'] + mods['dex'])
        self.builder.get_object('will').text("%d" % finTraits['resilience'] + mods['wis'])
        self.builder.get_object('speed').text("%dft." % self.npc['speed'])
        self.builder.get_object('experience').text("%d" % self.npc['experience'])

    def showAttributes(self):
        for trait,value in self.npc['traits'].items():
            box = self.builder.get_object("%s" % trait)
            box['state'] = 'normal'
            box.set(value)
            box['state'] = 'readonly'
        for attribute,value in self.npc['attributes'].items():
            box = self.builder.get_object("%s" % trait)
            box['state'] = 'normal'
            box.delete(0, "end")
            box.insert("end", "%d" % self.npc['attributes'][attribute])
            box['state'] = 'readonly'
        

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
traitTables = {}
with open("savedNPCs.json") as saveFile:
    try:
        npcs = json.loads(saveFile.read())
    except:
        pass
with open("traits.json") as saveFile:
    try:
        traitTables = json.loads(saveFile.read())
    except:
        pass

def d20():
    return randint(0,19)

if __name__ == '__main__':
    app = RootWindow()
    app.run()
