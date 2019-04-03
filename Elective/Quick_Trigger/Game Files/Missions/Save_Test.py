import os
dir_path = os.path.dirname(os.path.realpath(__file__)) #Gets current file directory

#Writing

input("Press enter to write")

text = "saved text"
text_saved = text.encode(encoding='UTF-8')
newFile = open(dir_path + "/saved.txt", "wb")
newFile.write(text_saved)
newFile = open(dir_path + "/saved.txt", "rb")

#Reading

input("Press enter to read")
print("")

readFile = open(dir_path + "/saved.txt", "rb")
text_read = readFile.read().decode(encoding='UTF-8')
print(text_read)
