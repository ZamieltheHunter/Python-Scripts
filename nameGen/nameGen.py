#!/usr/bin/python3
import tkinter as tk
import json
import pygubu
from npc import *
from random import randint
from math import floor
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
        self.elements = {}
        uiElements = ['genderBox', 'speciesBox','nameBox', 'listBox']
        for element in uiElements:
            self.elements[element] = self.builder.get_object(element)
        self.elements['genderBox'].current(0)
        self.elements['speciesBox'].current(0)
        self.children = {}
        for name,npc in npcs.items():
            self.elements['listBox'].insert("end", name)
            npcs[name] = NPC(name, npc)
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.onClose)

    def setGenderBox(self, event=None):
        if (self.elements['speciesBox'].get() in ['Rootwalker', 'Unborn', 'Drake']):
            self.elements['genderBox'].set('Both/Either/Other/None')
            self.elements['genderBox'].state(['disabled'])
        else:
            self.elements['genderBox'].state(['readonly'])

    def addNPC(self):
        name = self.elements['nameBox'].get()
        npcs[name] = NPC(name, {"gender" : self.elements['genderBox'].get(), "species" : self.speciesBox.get()})
        self.elements['listBox'].insert("end", name)

    def deleteNPC(self):
        for name in self.elements['listBox'].curselection():
            self.dl = self.elements['listBox'].curselection()
            messagebox = MessageWindow("Delete " + self.elements['listBox'].get(name) + "?", self.remove, None, "Delete?", "Delete", "Cancel")

    def remove(self):
        del npcs[self.elements['listBox'].get(self.dl)]
        self.elements['listBox'].delete(self.dl)
        self.dl = None

    def openNPC(self):
        for entry in self.elements['listBox'].curselection():
            name = self.elements['listBox'].get(entry)
            self.children[name] = NPCWindow(npcs[name])
            self.children[name].run()

    def makeName(self):
        gender = self.elements['genderBox'].current()
        equation = formatTable[self.elements['speciesBox'].current()][d20()]
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
        self.elements['nameBox'].delete(0,'end')
        self.elements['nameBox'].insert(0,final)
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
        self.elements = {}
        uiList = ['threatLabel', 'nameBox', 'textArea', 'genderBox', 'speciesBox', 'toggleButton',
                'threatBox', 'reachBox', 'sizeBox', 'speedBox', 'typeBox']
        for element in uiList:
            self.elements[element] = self.builder.get_object(element)
        self.elements['nameBox'].insert("end", self.npc['name'])
        self.elements['textArea'].insert("end", self.npc['text'])
        self.elements['genderBox'].set(self.npc['gender'])
        self.elements['speciesBox'].set(self.npc['species'])
        self.elements['reachBox'].set(self.npc['reach'])
        self.elements['sizeBox'].set(self.npc['size'])
        self.elements['speedBox'].set(self.npc['speed'])
        self.elements['typeBox'].set(self.npc['type'])
        self.elements['threatBox'].current(0)
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
        npcs[self.npc['name']]['attributes'] = self.npc['attributes']
        self.quit()

    def toggleEdit(self, event = None):
        if self.elements['speciesBox'].state() == ("disabled",):
            for element in self.elements:
                if 'Box' in element:
                    self.elements[element]['state'] = 'readonly'
            self.elements['speciesBox']['state'] = 'readonly'
            self.elements['genderBox']['state'] ='readonly'
            self.elements['nameBox']['state'] = 'normal'
            for trait in self.npc['traits']:
                try:
                    self.builder.get_object(trait).grid()
                    self.builder.get_object("%sEntry" % trait).grid_remove()
                except:
                    print("%sEntry not found" % trait)
            for attribute in self.npc['attributes']:
                entry = self.builder.get_object('%sEntry' % attribute)
                entry['state'] = 'normal'
                entry.delete(0,"end")
                entry.insert("end", "{}".format(self.npc['attributes'][attribute]))

            self.elements['threatLabel'].lower()
            self.elements['threatBox'].grid_remove()
            self.elements['toggleButton']['text'] = "Display"
            self.showAttributes()
        else: 
            for element in self.elements:
                if 'Box' in element:
                    self.elements[element]['state'] = 'disabled'
            self.elements['speciesBox']['state'] = 'disabled'
            self.elements['genderBox']['state'] ='disabled'
            self.elements['nameBox']['state'] = 'disabled'
            for trait in self.npc['traits']:
                try:
                    self.builder.get_object("%sEntry" % trait).grid()
                    self.builder.get_object(trait).grid_remove()
                except:
                    print("%sEntry not found" % trait)
            for attribute in self.npc['attributes']:
                entry = self.builder.get_object('%sEntry' % attribute)
                entry['state'] = 'normal'
                entry.delete(0,"end")
                entry.insert("end", "%d" % int((int(self.npc['attributes'][attribute]) - 10) / 2))
                self.builder.get_object("%sEntry" % attribute)['state'] = 'readonly'
            self.elements['threatLabel'].lift()
            self.elements['threatBox'].grid()
            self.elements['threatBox'].current(0)
            self.elements['toggleButton']['text'] = "Edit"
            self.updateDisplay()

    def rename(self, event = None):
        oldName = self.npc['name']
        newName = self.elements['nameBox'].get()
        if newName not in npcs:
            self.npc['name'] = newName
            npcs[newName] = self.npc
            del npcs[oldName]
        else:
            self.elements['nameBox'].delete(0,"end")
            self.elements['nameBox'].insert("end", oldName)

    def updateAttributes(self, event = None):
        exp = 0
        self.npc['gender'] = self.elements['genderBox'].get()
        self.npc['species'] = self.elements['speciesBox'].get()
        self.npc['speed'] = self.elements['speedBox'].get()
        exp += max([0, (int(self.npc['speed']) - 30) / 10])
        self.npc['size'] = self.elements['sizeBox'].get()

        for attribute in self.npc['attributes']:
            self.npc['attributes'][attribute] = self.builder.get_object("%sEntry" % attribute).get()
            exp += max([0, int(self.npc['attributes'][attribute]) - 10])
        for trait in self.npc['traits']:
            self.npc['traits'][trait] = self.builder.get_object(trait).get()
            exp += int(self.npc['traits'][trait])
        self.npc['text'] = self.elements['textArea'].get("1.0","end").strip()
        self.npc['experience'] = exp

    def updateDisplay(self, event = None):
        mods = {}
        finTraits = {}
        for trait, value in self.npc['traits'].items():
            box = self.builder.get_object("%sEntry" % trait)
            table = int(traitTables[trait])
            traitValue = int(value) - 1
            threat = int(self.elements['threatBox'].get())
            box['state'] = "normal"
            box.delete(0,"end")
            finTraits[trait] = 0 if traitValue == -1 else int(traitTables['tables'][table][traitValue][threat])
            box.insert("end", "{}".format(finTraits[trait]))
            box['state'] = "readonly"
        for attribute, value in self.npc['attributes'].items():
            box = self.builder.get_object('%sEntry' % attribute)
            box['state'] = "normal"
            box.delete(0, "end")
            if int(value) >= 10:
                mods[attribute] = int((int(value) - 10) / 2)
                sign = "+"
            else:
                mods[attribute] = floor((int(value) - 10) / 2)
                sign = ""
            box.insert("end", "{}{}".format(sign, mods[attribute]))
            box['state'] = "readonly"
        calcs = {}
        calcs['initMod'] = finTraits['initiative'] + mods['dex']
        calcs['healthSave'] = finTraits['health'] + mods['con']
        calcs['melee'] = finTraits['attack'] + mods['str']
        calcs['ranged'] = finTraits['attack'] + mods['dex']
        calcs['finDefense'] =finTraits['defense'] + mods['dex']
        calcs['fortitudeSave'] =finTraits['resilience'] + mods['con']
        calcs['reflexSave'] =finTraits['resilience'] + mods['dex']
        calcs['willSave'] = finTraits['resilience'] + mods['wis']
        for calc,value in calcs.items():
            if value > 0:
                sign = '+'
            else:
                sign = ""
            self.builder.get_object(calc)['text'] = "{}{}".format(sign, value)
        self.builder.get_object('experience')['text'] = "%d" % self.npc['experience']

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
            box.insert("end", "{}".format(self.npc['attributes'][attribute]))
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
