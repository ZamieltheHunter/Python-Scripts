#!/usr/bin/python3
import tkinter as tk
from tkinter import *
import json
import pygubu
from npc import *
from random import randint
from math import floor
import csv
import sys
import copy
import pprint

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
        npcs[name] = NPC(name, {"gender" : self.elements['genderBox'].get(), "species" : self.elements['speciesBox'].get()})
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
        if self.elements['speciesBox'].current() == "Other":
                final = "Unable to make name for Other"
        else :
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
            'threatUpdated' : self.updateDisplay,
            'openAttackWindow' : self.openAttackWindow
        }, npc['name'])
        self.npc = copy.deepcopy(npc)
        self.elements = {}
        uiList = ['threatLabel', 'nameBox', 'textArea', 'genderBox', 'speciesBox', 'toggleButton',
                'threatBox', 'reachBox', 'sizeBox', 'speedBox', 'typeBox', 'attackList']
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
        self.elements['attackWindow'] = None
        self.printAttackString()
        self.builder.get_object('spaceLabel1').lower()
        self.builder.get_object('spaceLabel2').lower()
        self.showAttributes()
        for trait in self.npc['traits']:
            try:
                self.builder.get_object(trait).grid_remove()
            except:
                print("%sEntry not found" % trait)
        self.toggleEdit()
    def okay(self, event = None):
        name = self.npc['name']
        npcs[name]['gender'] = self.npc['gender']
        npcs[name]['species'] = self.npc['species']
        npcs[name]['text'] = self.npc['text']
        npcs[name]['type'] = self.npc['type']
        npcs[name]['reach'] = self.npc['reach']
        npcs[name]['size'] = self.npc['size']
        npcs[name]['speed'] = self.npc['speed']
        npcs[name]['traits'] = self.npc['traits']
        npcs[name]['attributes'] = self.npc['attributes']
        npcs[name]['attackList'] = self.npc['attackList']
        self.quit()
    def printAttackString(self):
        attackString = "Name\tTo-Hit\tThreat\tDamage"
        for attackName,attack in self.npc['attackList'].items():
            attackAttr = self.npc['attributes']['str'] if attack['upgrades']['finesse']['state'] == 0 else self.npc['attributes']['dex']
            mod = int((int(attackAttr) - 10) / 2)
            threat = int(self.elements['threatBox'].get())
            traitMod =  int(traitTables['tables'][1][int(self.npc['traits']['attack']) - 1][threat])
            bonus = mod + traitMod
            sizeCat = self.npc['size'][0]
            dieMod = traitTables['naturalAttacks'][attack['type']]['die'] + traitTables['sizeMod'][sizeCat]
            dmgDie = traitTables['naturalAttacks']['dice'][dieMod]
            numDice = int(dmgDie[0])
            dieType = dmgDie[1:]
            if int(attack['grade']) == 5:
                numDice *= 3
            elif int(attack['grade']) > 2:
                numDice *= 2
            dmgDie = "{}{}".format(numDice, dieType)

            dmgBonus = int((int(self.npc['attributes']['str']) -10) / 2)
            if dmgBonus > 0:
                dmgBonus = "+{}".format(dmgBonus)
            elif dmgBonus < 0:
                dmgBonus = "-{}".format(dmgBonus)
            dmgType = "lethal" if attack['upgrades']['alternatedamage']['state'] == 0 else attack['upgrades']['alternatedamage']['value']
            damage = "{}{}({})".format(dmgDie, dmgBonus, dmgType)

            critThreat = traitTables['naturalAttacks'][attack['type']]['threat']

            if critThreat != 0:
                critThreat -= int(attack['grade']) % 2
                threatRange = "{}-20".format(critThreat) if critThreat != 20 else "20"
            else:
                threatRange = "-"
            attackString += "\n{}\t{}\t{}\t{}".format(attackName, bonus, threatRange, damage)
        self.elements['attackList'].delete('1.0', "end")
        self.elements['attackList'].insert("end", attackString)

    def toggleEdit(self, event = None):
        if self.elements['speciesBox'].state() == ("disabled",):
            for element in self.elements:
                if 'Box' in element:
                    if element != 'threatBox':
                        self.elements[element]['state'] = 'readonly'
                    else :
                        self.elements[element]['state'] = 'disabled'
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
                    if element != 'threatBox':
                        self.elements[element]['state'] = 'disabled'
                    else :
                        self.elements[element]['state'] = 'readonly'
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
        self.npc['gender'] = self.elements['genderBox'].get()
        self.npc['species'] = self.elements['speciesBox'].get()
        self.npc['speed'] = self.elements['speedBox'].get()
        self.npc['size'] = self.elements['sizeBox'].get()
        self.npc['reach'] = self.elements['reachBox'].get()
        self.npc['type'] = self.elements['typeBox'].get()
        npcType = traitTables['types'][self.npc['type']]
        for attribute in self.npc['attributes']:
            attEntry = self.builder.get_object("{}Entry".format(attribute))
            if 'attributeLimits' in npcType:
                if attribute in  npcType['attributeLimits']:
                    if int(attEntry.get()) > npcType['attributeLimits'][attribute]:
                        attEntry.delete(0, "end")
                        attEntry.insert("end", npcType['attributeLimits'][attribute])
            self.npc['attributes'][attribute] = attEntry.get()
        for trait in self.npc['traits']:
            traitEntry = self.builder.get_object(trait)
            if 'traitLimits' in npcType:
                if trait in npcType['traitLimits']:
                    if int(traitEntry.get()) > npcType['traitLimits'][trait]:
                        traitEntry.delete(0, "end")
                        traitEntry.insert("end", npcType['traitLimits']['trait'])
            self.npc['traits'][trait] = traitEntry.get()

        self.npc['text'] = self.elements['textArea'].get("1.0","end").strip()
        self.calculateXP()

    def calculateXP(self):
        xp = 0
        xp += max([0, (int(self.npc['speed']) - 30) / 10])
        xp += int(self.npc['reach']) - 1
        xp += traitTables['types'][self.npc['type']]['exp']
        for attribute in self.npc['attributes']:
            xp += max([0, int(self.npc['attributes'][attribute]) - 10])
        for trait in self.npc['traits']:
            xp += int(self.npc['traits'][trait])
        for attackName, attack in self.npc['attackList'].items():
            xp += 2 * int(attack['grade'])
            for upgrade, kind in traitTables['attackUpgrades'].items():
                if kind == 'graded':
                    xp += 2 * attack['upgrades'][upgrade]['state'] * attack['upgrades'][upgrade]['value']
                else: 
                    xp += 2 * attack['upgrades'][upgrade]['state']
        self.npc['experience'] = xp




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
            finTraits[trait] = 0 if traitValue == -1 else int(traitTables['tables'][table][traitValue][threat - 1])
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
        expLabel = self.builder.get_object('experience')
        self.builder.get_object('experience')['text'] = "{}".format(self.npc['experience'])
        self.printAttackString()

    def showAttributes(self):
        for trait,value in self.npc['traits'].items():
            box = self.builder.get_object("%s" % trait)
            box['state'] = 'normal'
            box.set(value)
        for attribute,value in self.npc['attributes'].items():
            box = self.builder.get_object("%sEntry" % attribute)
            box['state'] = 'normal'
            box.delete(0, "end")
            box.insert("end", "{}".format(self.npc['attributes'][attribute]))
        self.updateAttributes()

    def openAttackWindow(self):
        if self.elements['attackWindow'] == None:
            self.elements['attackWindow'] = AttackWindow(self)
        else :
            self.elements['attackWindow'].lift()

    def updateAttackList(self, attackList):
        self.npc['attackList'] = attackList
        self.calculateXP()
        self.updateDisplay()

    def closeAttackWindow(self):
        self.elements['attackWindow'].quit()
        self.elements['attackWindow'] = None
        
class AttackWindow(Application):
    def __init__(self, parent):
        super().__init__("attackWindow",{
                "updateAttack"  : self.updateAttack,
                "switchAttack"  : self.switchAttack,
                "close"         : self.close,
                "newAttack"     : self.newAttack,
                "deleteAttack"  : self.deleteAttack,
                "updateCheck"   : self.updateCheck,
                "valueUpdate"   : self.valueUpdate
            }, 
            "Attacks")
        self.listBox = self.builder.get_object('attackList')
        self.gradeBox = self.builder.get_object('gradeBox')
        self.typeBox = self.builder.get_object('typeBox')
        self.current = None

        self.props = {
                'attacks'       : parent.npc['attackList'],
                'parent'        : parent,
                'checks'        : {}
            }
        self.props['checks']['natural'] = IntVar()
        self.builder.get_object('natural')['variable'] = self.props['checks']['natural']
        self.props['checks']['natural'].set(1)

        for attack in self.props['attacks']:
            self.listBox.insert("end", attack)
        for upgrade in traitTables['attackUpgrades']:
            self.props['checks'][upgrade] = IntVar()
            self.props['checks'][upgrade].set(0)
            self.builder.get_object(upgrade)['variable'] = self.props['checks'][upgrade]

        self.mainwindow.protocol("WM_DELETE_WINDOW", self.close)

    def newAttack(self, event = None):
            messagebox = MessageWindow("Name your new attack", self.addAttack, None, "New Attack", "Okay", "Cancel", True)
        
    def addAttack(self, name):
        if name in self.props['attacks']:
            messageBox = MessageWindow("Already has attack with that name choose another", self.addAttack, None, "New Attack", "Okay", "Cancel", True)
        else :
            self.props['attacks'][name] = {"type" : "Bite", "grade" : 1, "upgrades" : {}}
            for upgrade in traitTables['attackUpgrades']:
                self.props['attacks'][name]['upgrades'][upgrade] = { "state" : 0, "value": None}
            self.listBox.insert("end", name)
            self.current = name
            if len(self.listBox.curselection()) != 0:
                self.listBox.selection_clear(self.listBox.curselection())
            self.listBox.selection_set(self.listBox.size() - 1)
            self.switchAttack()

    def deleteAttack(self, event = None):
        del self.props['attacks'][self.listBox.get("active")]
        self.listBox.delete("active")
        self.current = None

    def updateAttack(self, event = None):
        if self.current != None:
            self.props['attacks'][self.current]['type'] = self.typeBox.get()
            self.props['attacks'][self.current]['grade'] = self.gradeBox.get()

    def switchAttack(self, event = None):
        if len(self.listBox.curselection()) == 1:
            self.current = self.listBox.get(self.listBox.curselection())
        if self.current != None:
            self.typeBox.set(self.props['attacks'][self.current]['type'])
            self.gradeBox.set(self.props['attacks'][self.current]['grade'])
            for upgrade,kind in traitTables['attackUpgrades'].items():
                self.props['checks'][upgrade].set(self.props['attacks'][self.current]['upgrades'][upgrade]['state'])
                value = self.props['attacks'][self.current]['upgrades'][upgrade]['value']
                value = value if value else ""
                if kind == 'graded' or kind == 'entry':
                    entry = self.builder.get_object("{}Entry".format(upgrade))
                    entry['state'] = 'normal'
                    entry.delete(0, "end")
                    entry.insert("end", value)
                    if self.props['checks'][upgrade].get() == 0:
                        entry['state'] = 'disabled'
                elif kind == 'combo':
                    box = self.builder.get_object("{}Box".format(upgrade))
                    box['state'] = 'readonly'
                    box.set(value)
                    if self.props['checks'][upgrade].get() == 0:
                        box['state'] = 'disabled'


    def updateCheck(self, event = None):
        if self.current != None:
            for upgrade,kind in traitTables['attackUpgrades'].items():
                if kind == 'graded' or kind == 'entry':
                    if self.props['checks'][upgrade].get() == 1:
                        self.builder.get_object("{}Entry".format(upgrade))['state'] = "normal"
                    else:
                        self.builder.get_object("{}Entry".format(upgrade))['state'] = "disabled"
                elif kind == 'combo':
                    if self.props['checks'][upgrade].get() == 1:
                        self.builder.get_object("{}Box".format(upgrade))['state'] = 'readonly'
                    else:
                        self.builder.get_object("{}Box".format(upgrade))['state'] = 'disabled'
                self.props['attacks'][self.current]['upgrades'][upgrade]['state'] = self.props['checks'][upgrade].get()

                        
    def valueUpdate(self, event = None):
        for upgrade, kind in traitTables['attackUpgrades'].items():
            if self.props['checks'][upgrade].get() == 1:
                if kind == 'entry':
                    self.props['attacks'][self.current]['upgrades'][upgrade]['value'] = self.builder.get_object("{}Entry".format(upgrade)).get()
                elif kind == 'graded':
                    self.props['attacks'][self.current]['upgrades'][upgrade]['value'] = int(self.builder.get_objects("{}Entry".format(upgrade)).get())
                elif kind == 'combo':
                    self.props['attacks'][self.current]['upgrades'][upgrade]['value'] = self.builder.get_object("{}Box".format(upgrade)).get()
        self.builder.get_object('attackList').focus()

    def close(self):
        self.props['parent'].updateAttackList(self.props['attacks'])
        self.props['parent'].closeAttackWindow()


class MessageWindow(Application):
    def __init__(self, question, callbackYes, callbackNo, title = "Message Box", labelYes = 'Yes', labelNo = 'No', entry = False):
        super().__init__('messageWindow', {
                'yesClick' : self.yes,
                'noClick' : self.no,
            },title)
        self.callbackYes = callbackYes
        self.callbackNo = callbackNo
        self.entry = entry
        self.builder.get_object('yesButton')['text']  = labelYes
        self.builder.get_object('noButton')['text'] = labelNo
        self.builder.get_object('message')['text'] = question
        if self.entry:
            self.builder.get_object('entryBox').focus()
        else:
            self.builder.get_object('entryBox').grid_remove()
        
    def yes(self, event = None):
        if self.entry:
            value = self.builder.get_object('entryBox').get()
        self.quit()
        if self.callbackYes != None:
            if self.entry:
                self.callbackYes(value)
            else:
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
