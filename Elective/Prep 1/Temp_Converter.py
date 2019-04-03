#Max Clark

def FToC(fah: int):
    cel = (fah - 32)*5/9
    return cel

def CToF(cel: int):
    fah = cel/(5/9) + 32
    return fah

print("")
print("This is the Fahrenheit/Celsuis Converter")
print("")
repeat = True

while repeat:
    correctStr = False
    correctAns = False
    while not correctStr:
        desired = input("Would you like to convert to fahrenheit or celsius (type 'f' or 'c'): ")
        if desired == "c":
            correctStr = True
            f = float(input("Type the value of fahrenheit: "))
            c = FToC(f)
            print(f, "ºF is equal to ", c, "ºC")
        elif desired == "f":
            correctStr = True
            c = float(input("Type the value of celsius: "))
            f = CToF(c)
            print(c, "ºC is equal to ", f, "ºF")
            
    while not correctAns:
        again = input("Do you want to convert again? (type 'y' or 'n'): ")
        if again == "n":
            exit()
        elif again == "y":
            correctAns = True
            print("")
    
