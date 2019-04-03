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
    
    while not correctAns:
        again = input("Would you like to calculate again? (type 'y' or 'n') ")
        if again == "n":
            exit()
        elif again == "y":
            correctAns = True
            print("")
