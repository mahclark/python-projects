import pygame
import os
import time
import math
import random
from random import randint
import sys
from ctypes import windll

def roll_text(string):
    text = ''
    for i in range(len(string)):
        print(string[i], end='', flush=True)
        time.sleep(0.04)

os.system('mode con: cols=70 lines=50')

dir_path = os.path.dirname(os.path.realpath(__file__))

try:
    lockFile = open(dir_path + "/Game Files/Saves/lock.txt", "rb")
    txtRead = lockFile.read().decode(encoding='UTF-8')
except:
    txtRead = "failed"

chp1 = txtRead[0]
chp2 = txtRead[1]
chp3 = txtRead[2]

lockSave = chp1 + "1" + chp3

tsaved = lockSave.encode(encoding='UTF-8')
newFile = open(dir_path + "/Game Files/Saves/lock.txt", "wb")
newFile.write(tsaved)
newFile = open(dir_path + "/Game Files/Saves/lock.txt", "rb")

try:
    skipFile = open(dir_path + "/Game Files/Saves/skip.txt", "rb")
    binRead = skipFile.read().decode(encoding='UTF-8')
except:
    binRead = "1"

if 'idlelib.run' in sys.modules:
    print("Run in CMD for optimised experience.")
    print("")


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
    skipFile = open(dir_path + "/Game Files/Saves/skip.txt", "rb")
    binRead = skipFile.read().decode(encoding='UTF-8')
except:
    binRead = "1"

if binRead == "1":
    time.sleep(1)
    roll_text("(Press enter to open newspaper)")
    input("")
    print("")
    print("")
    print("---------------------------Newspaper Opened---------------------------")
    time.sleep(1)
    roll_text("September 2nd, 1943")
    time.sleep(1)
    print("")
    print("")
    roll_text("Hitler Assassinated!")
    time.sleep(1)
    roll_text(" The War is Won!")
    time.sleep(1)
    print("")
    print("")
    print("---------------------------Newspaper Closed---------------------------")
    print("")
    time.sleep(1)
    roll_text("(Press enter to open newspaper)")
    input("")
    print("")
    print("")
    print("---------------------------Newspaper Opened---------------------------")
    time.sleep(1)
    roll_text("September 5th, 1943")
    time.sleep(1)
    print("")
    print("")
    roll_text("Disease Outbreak in Germany.")
    time.sleep(1)
    print("")
    roll_text("It is spreading amongst the dead, causing partial brain activity,")
    print("")
    roll_text("allowing some movement and cannibalism.")
    time.sleep(1)
    print("")
    print("")
    print("---------------------------Newspaper Closed---------------------------")
else:
    roll_text("Newspaper skipped.")
time.sleep(1)
print("")
roll_text("(Press enter to load next brief)")
input("")
exec(open(dir_path + "/Game Files/Missions/Mission_3.py").read(), globals())
