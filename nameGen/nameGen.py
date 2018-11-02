#!/usr/bin/python3
import tkinter as tk
import pygubu
from npc import *
from random import randint
import csv
import sys

class Application:
    def __init__(self):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('ttkLayout.ui')
        self.mainwindow = builder.get_object('baseWindow')
        builder.connect_callbacks(self)
    def run(self):
        self.mainwindow.mainloop()
    def quit(self):
        self.mainwindow.quit()
    def setGenderBox(self, event=None):
        print("Here")
        genderBox = app.builder.get_object('genderBox')
        speciesBox = app.builder.get_object('speciesBox')
        if (speciesBox.get() in ['Rootwalker', 'Unborn', 'Drake']):
            genderBox.set('Both/Either/Other/None')
            genderBox.state(['disabled'])
        else:
            genderBox.state(['!disabled'])

if __name__ == '__main__':
    app = Application()
    app.run()
names = list(npcs)

#
#  def d20():
#      return randint(0,19)
#
#  def onClose():
#      if messagebox.askokcancel("Quit", "Do you wish to exit?"):
#          root.destroy()
#
#  def addNPC():
#      name = nameBox.get()
#      names.append(name)
#      npcs[name] = NPC(name, {"gender" : genderBox.get(), "species" : speciesBox.get()})
#      listBox.insert(END, name)
#
#  def deleteNPC():
#      for name in listBox.curselection():
#          if messagebox.askokcancel("Confirm Delete", "Delete " + listBox.get(name) + "?"):
#              npcs[listBox.get(name)].delete()
#
#      listBox.delete(0, END)
#      for npc in npcs:
#          listBox.insert(END, npc)
#
#  def editNPC():
#      for entry in listBox.curselection():
#          name = listBox.get(entry)
#          npcs[name].edit()
#
#  def makeName():
#      gender = genderBox.current()
#      equation = formatTable[speciesBox.current()][d20()]
#      final = ""
#      first = 0
#      for symbol in equation:
#          if("A" <= symbol < "P" or symbol == "X"):
#              sym = ord(symbol) - 65
#              part = ''
#              if(sym < 10):
#                  part = nameTable[ord(symbol) - 65][d20()]
#              elif(sym == 11 or sym == 12):
#                  if(gender == 2):
#                      gender = randint(0,1)
#                  part = nameTable[sym][d20()].split("/")[gender];
#              elif(symbol == "X"):
#                  part = str(randint(0,10000))
#              else:
#                  part = nameTable[sym][d20()].split("/")[first]
#              
#              if(first != 0):
#                  final += part.lower()
#              else :
#                  final += part
#          else:
#              final += symbol
#
#          if(symbol == " "):
#              first = 0
#          else:
#              first = 1
#      nameBox.delete(0,'end')
#      nameBox.insert(0,final)
#
#  if getattr(sys, 'frozen', False):
#      formatFile = sys._MEIPASS + "/format.csv"
#      nameFile = sys._MEIPASS + "/sorted.csv"
#  else:
#      formatFile = "format.csv"
#      nameFile = "sorted.csv"
#  with open(nameFile, "r") as table:
#      reader = csv.reader(table)
#      nameTable = [[c for c in r] for r in reader]
#  with open(formatFile, "r") as table:
#      reader = csv.reader(table)
#      formatTable =[[c for c in r] for r in reader]
#
#  generatedName = ''
#  speciesBox.current(0)
#  speciesBox.bind("<<ComboboxSelected>>", setGenderBox)
#  genderBox.current(0)
#
#  for name in names:
#      listBox.insert(END, name)
#      npcs[name] = NPC(name, npcs[name])
#
