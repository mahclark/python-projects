#Max Clark

print("")
print("This is the Container Calculator")
print("It will calculate how many boxes will fit inside a larger container.")
print("")

repeat = True

while repeat:
    correctAns = False
    cW = float(input("Enter container width: "))
    cD = float(input("Enter container depth: "))
    cH = float(input("Enter container height: "))
    
    bW = float(input("Enter box width: "))
    bD = float(input("Enter box depth: "))
    bH = float(input("Enter box height: "))
    
    timesW = int(cW/bW)
    timesD = int(cD/bD)
    timesH = int(cH/bH)

    times = timesW*timesD*timesH

    print("")
    if times != 1:
        print(times, "boxes will fit in the container in that orientation.")
    else:
        print(times, "box will fit in the container in that orientation.")
    print("")

    while not correctAns:
        again = input("Would you like to calculate again? (type 'y' or 'n') ")
        if again == "n":
            exit()
        elif again == "y":
            correctAns = True
            print("")
