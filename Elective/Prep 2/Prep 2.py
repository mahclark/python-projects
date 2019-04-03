#1
print("Challenge 1")
print("")
for i in range(9):
    print("*",end='')
print("*")

#2
input("(press enter to continue)")
print("")
print("Challenge 2")
print("")
for i in range(9):
    print("*",end='')
    print("   ",end='')
print("*")
for i in range(4):
    print("*",end='')
    print("        ",end='')
print("*")
for i in range(18):
    print("*",end='')
    print(" ",end='')
print("*")

#3
input("")
print("")
print("Challenge 3")
print("")
for i in range(10):
    for i in range(9):
        print("*  ",end='')
    print("*")
print("")

#4
input("")
print("")
print("Challenge 4")
print("")
for i in range(10):
    for i in range(4):
        print("*     ",end='')
    print("*")
print("")

#5
input("")
print("")
print("Challenge 5")
print("")
for i in range(5):
    for i in range(20):
        print("*  ",end='')
    print("*")
print("")

#6
input("")
print("")
print("Challenge 6")
print("")
for i in range(10):
    for n in range(9):
        print(n," ",end='')
    print("9")
print("")

#7
input("")
print("")
print("Challenge 7")
print("")
for i in range(9):
    for n in range(9):
        print(i," ",end='')
    print(i)
for i in range(10):
    print("9",end='')
print("")

#8
input("")
print("")
print("Challenge 8")
print("")
for j in range(10):
    for n in range(j):
        print(n, end='')
        if j != 1 and j-1>n:
            for x in range(round(120/(j-1) - 1)):
                print(" ",end='')
    print("")
for i in range(10):
    print(i,end='')
print("")
print("")
print("Note:")
print("Please enter full screen.")
print("The line ending in 7 is not in line. This is because 7 is not a factor of 120. In order to make it in line, the whole picture would need to be 840 characters wide. This requires a monitor resolution width of at least 4290 pixels, if you exclude the window borders (given you can reduce the font size to 7).")
print("")
print("")
input("Here it is anyway, in case your monitor has a high enough resolution (or your combined width resolution for your multiple monitor setup is greater than 4290):")
print("")
for j in range(10):
    for n in range(j):
        print(n, end='')
        if j != 1 and j-1>n:
            for x in range(int(round(840/(j-1) - 1))):
                print(" ",end='')
    print("")
for i in range(10):
    print(i,end='')
