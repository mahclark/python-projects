def getd(n):
    ds = []
    n = str(n)
    for i in range(len(n)):
        ds.append(int(n[i]))
    return ds

def getn(d):
    n = 0
    for i in range(len(d)):
        n += d[i]*pow(10,len(d) - i - 1)
    return n

def isprime(n):
    if n == 1: return False
    if n == 2: return True
    if n == 3: return True
    if n % 2 == 0: return False
    if n % 3 == 0: return False
    i = 5
    w = 2
    while i * i <= n:
        if n % i == 0: return False
        i += w
        w = 6 - w
    return True

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

def read(path):
    newFile = open(dir_path + path, "rb")
    txtRead = newFile.read().decode(encoding='UTF-8')

    return txtRead
     
