#Max Clark
done = False
while not done:
    print("")
    prep = input("Which prep part do you want to use? (type 'a', 'b', 'c' or 'x' to exit): ")
    if prep == "a":
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
                print("")
                again = input("Do you want to convert again? (type 'y' or 'n'): ")
                if again == "n":
                    correctAns = True
                    repeat = False
                elif again == "y":
                    correctAns = True
                    print("")

    elif prep == "b":
        #Max Clark
        
        print("")
        print("This is the Trapezoid Area Calculator")
        print("")
        
        repeat = True
        
        while repeat:
            correctAns = False
            a = float(input("Enter the top length: "))
            b = float(input("Enter the base length: "))
            h = float(input("Enter the height: "))
            area = (a + b)*h/2
            print("The area is ", area, ".")
            print("")
            
            while not correctAns:
                again = input("Would you like to calculate again? (type 'y' or 'n'): ")
                if again == "n":
                    correctAns = True
                    repeat = False
                elif again == "y":
                    correctAns = True
                    print("")
        
    elif prep == "c":
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
                again = input("Would you like to calculate again? (type 'y' or 'n'): ")
                if again == "n":
                    correctAns = True
                    repeat = False
                elif again == "y":
                    correctAns = True
                    print("")

    elif prep == "x":
        exit()
