from random import choice, randint
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

def read(path):
	newFile = open(dir_path + path, "rb")
	txtRead = newFile.read().decode(encoding='UTF-8')

	return txtRead

first = []
suffix = []
prefix = []
second = []

for name in read("\\name_data\\stations_first.txt").splitlines():
	if not name in first:
		first.append(name)

for name in read("\\name_data\\stations_suffix.txt").splitlines():
	if not name in suffix:
		suffix.append(name)

for name in read("\\name_data\\stations_prefix.txt").splitlines():
	if not name in prefix:
		prefix.append(name)

for name in read("\\name_data\\stations_second.txt").splitlines():
	if not name in second:
		second.append(name)

def generateStation():
	word2 = None
	if randint(0,3) == 0:
		word1 = choice(first)
	else:
		word1 = choice(prefix) + choice(suffix)

	if randint(0,1) == 0:
		word2 = choice(second)

	if word2 == None:
		return word1
	return word1 + " " + word2

if __name__ == "__main__":
	for _ in range(10):
		print(generateStation())