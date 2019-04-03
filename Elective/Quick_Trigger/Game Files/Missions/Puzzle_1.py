import pygame
import math
import time
import random
from random import randint
import sys
from ctypes import windll
from math import atan2, degrees, pi
import os

os.system('mode con: cols=70 lines=50')

dir_path = os.path.dirname(os.path.realpath(__file__))

if 'idlelib.run' in sys.modules:
    print("Run in CMD for optimised experience.")
    print("")
    idle = True
else:
    idle = False

try:
    lockFile = open(dir_path + "/Game Files/Saves/been.txt", "rb")
    txtRead = lockFile.read().decode(encoding='UTF-8')
except:
    txtRead = "failed"

chp1 = txtRead[0]
chp2 = txtRead[1]
chp3 = txtRead[2]

lockSave = chp1 + "1" + chp3

tsaved = lockSave.encode(encoding='UTF-8')
newFile = open(dir_path + "/Game Files/Saves/been.txt", "wb")
newFile.write(tsaved)
newFile = open(dir_path + "/Game Files/Saves/been.txt", "rb")

if chp2 == "0":
    saved = "1"
    bsaved = saved.encode(encoding='UTF-8')
    newFile = open(dir_path + "/Game Files/Saves/skip.txt", "wb")
    newFile.write(bsaved)
    newFile = open(dir_path + "/Game Files/Saves/skip.txt", "rb")

else:
    ans = input("Would you like to skip brief? (y or n): ")
    print("")
    if ans.lower() == "y":
        saved = "0"
    else:
        saved = "1"
    bsaved = saved.encode(encoding='UTF-8')
    newFile = open(dir_path + "/Game Files/Saves/skip.txt", "wb")
    newFile.write(bsaved)
    newFile = open(dir_path + "/Game Files/Saves/skip.txt", "rb")

try:
    newFile = open(dir_path + "/Game Files/Saves/skip.txt", "rb")
    binRead = newFile.read(1).decode(encoding='UTF-8')
except:
    binRead = "1"

def roll_text(string):
    text = ''
    for i in range(len(string)):
        print(string[i], end='', flush=True)
        time.sleep(0.04)

os.system('mode con: cols=70 lines=50')

if binRead == "1":
    time.sleep(1)
    roll_text("Loading brief")
    time.sleep(0.5)
    print(".",end='', flush=True)
    time.sleep(0.5)
    print(".",end='', flush=True)
    time.sleep(0.5)
    print(".")
    time.sleep(3)
    roll_text("Brief loaded.")
    time.sleep(1)
    roll_text(" (Press enter to open brief)")
    input("")
    print("")
    print("")
    print("-----------------------------Brief Opened-----------------------------")
    time.sleep(1)
    roll_text("Agent 47")
    time.sleep(1)
    print("")
    print("")
    roll_text("Mission 1")
    time.sleep(1)
    print("")
    print("")
    roll_text("To reach the vantage point, you must bypass high German security.")
    time.sleep(1)
    roll_text(" To")
    print("")
    roll_text("get through the door, the Germans have developed an extremely complex puzzle that only Nazis know the answer to.")
    time.sleep(1)
    roll_text(" Your objective is to solve this puzzle and breach the security. No other agent has yet managed   this.")
    time.sleep(1)
    print("")
    print("")
    print("-----------------------------Brief Closed-----------------------------")
    roll_text("(Press enter when ready)")
else:
    roll_text("Brief skipped.")
    roll_text(" (Press enter when ready)")
    
input("")
print("")
os.system('cls')

print("Highly sofisticated German security:")
print("")
print("**********************************************")
print("*                                            *")
print("* Velcome to ONE PLAYER Noughtz unt Krosses. *")
print("*                                            *")
print("**********************************************")
print("")
print("Please note this is ONE PLAYER.")
print("")
print("(Press enter to continue)")
input("")
os.system('cls')
def print_inst():
    if not idle:
        print("Highly sofisticated German security:")
        print("")
        print("**********************************************")
        print("*                                            *")
        print("* Velcome to ONE PLAYER Noughtz unt Krosses. *")
        print("*                                            *")
        print("**********************************************")
        print("")
        print("Please note this is ONE PLAYER.")
        print("")
        print("You must place Xs on the grid. You must make a line.")
        print("Step 1: Enter the column number (1, 2 or 3).")
        print("Step 2: Enter the row number (1, 2 or 3).")
        print("Step 3: Press enter to submit position, e.g. 32.")
        print("")
print_inst()
if idle:
        print("You must place Xs on the grid. You must make a line.")
        print("Step 1: Enter the column number (1, 2 or 3).")
        print("Step 2: Enter the row number (1, 2 or 3).")
        print("Step 3: Press enter to submit position, e.g. 32.")
        print("")
print("You have 100 turns.")
print("")
print("(Press enter when ready)",end='')
input("")
os.system('cls')
print_inst()
print("")

print("  1 2 3")
print("")
for i in range(3):
    print(str(i+1) + "  | | ")
    
done = False
been = []

while not done:
    wrong = True
    print("")
    while wrong:
        print("You have", 100-len(been), "turns remaining.")
        print("")
        inp1 = input("Enter column number : ")
        inp2 = input("Enter row number    : ")
        inp = inp1 + inp2
        try:
            if 3 >= int(inp[0]) > 0 and 3 >= int(inp[1]) > 0:
                wrong = False
            if len(inp) >= 3:
                wrong = True
        except:
            wrong = True
        if wrong == True:
            print("invalid input")
            
    os.system('cls')
    print_inst()
    print("")
    
    if inp not in been:
        been.append(inp)

    #Drawing Table
    print("  1 2 3")
    print("")
    for y in range(3):
        print(str(y+1) + " ",end='')
        for x in range(3):
            empty = True
            
            for place in been:
                if int(place[0])-1 == x and int(place[1])-1 == y and empty == True:
                    print("X",end='')
                    empty = False
                    
            if empty == True:
                print(" ",end='')
                
            if x != 2:
                print("|",end='')
            else:
                print("")
    
    #Detect Win

    countr = [0,0,0]
    countc = [0,0,0]
    countd = [0,0]
    
    for item in been:
        countr[int(item[1])-1] += 1
        countc[int(item[0])-1] += 1
        
        if item[0] == item[1]:
            countd[0] += 1
        if int(item[0]) + int(item[1]) == 4:
            countd[1] += 1

    for item in countr:
        if item == 3:
            done = True

    for item in countc:
        if item == 3:
            done = True
            
    for item in countd:
        if item == 3:
            done = True

print("")
print("Congratulations! You have breached security in " + str(len(been)) + " moves. The world")
print("record is 3 moves.")
time.sleep(1)
print("")
roll_text("(Press enter to load next brief)")
input("")
exec(open(dir_path + "/Game Files/Missions/Mission_2.py").read(), globals())
            
