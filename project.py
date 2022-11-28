import numpy as np
import sys
import cv2
import math
import random

def compress(a, A, compress):
    
    i = 0
    while(i < len(a)):    
        cur = a[i]
        count = 0
        while(a[i] == cur):
            count = count + 1
            i = i + 1
            if(i >= len(a)):
                break
        amount = math.ceil(count / compress)
        for j in range (0, amount):
            A.append(cur)

def shiftRange(A, pos):
   
    if(pos == "High"):
        for i in range(0, len(A)):
            A[i] = math.floor(A[i]/8) + 44
    elif(pos == "Mid"):
        for i in range(0, len(A)):
            A[i] = math.floor(A[i]/8) + 34
    elif(pos == "Bass"):
        for i in range(0, len(A)):
            A[i] = math.floor(A[i]/8) + 24 
        
def shiftMode(L, mode):
    
    C = 0
    Df = Cs = 1
    D =  2
    Ef = Ds = 3
    E = 4
    F = 5
    Gf = Fs = 6
    G = 7
    Af = Gs = 8
    A = 9
    Bf = As = 10
    B = 11

    '''
                    "C, Db, D,  Eb, E,  F,  Gb, G,  Ab, A,  Bb, B "
                    "0, 1,  2,  3   4,  5,  6,  7,  8,  9,  10, 11"
    '''
    Ionian      =   [C, C,  D,  D,  E,  F,  F,  G,  A,  A , B,  B]
    Lydian      =   [C, Fs, D,  E,  E,  Fs, Fs, G,  A,  A,  B, B]
    Mixolydian  =   [C, Bf, D,  E,  E,  F,  Bf, G,  A,  A,  Bf, Bf]
    
    Aeolian     =   [C, D,  D,  Ef, Ef, F,  G,  G,  Af, Af, Bf, Bf]
    Dorian      =   [C, D,  D,  Ef, Ef, F,  A,  G,  A,  A,  Bf, Bf]
    Phrygian    =   [C, Df, Df, Ef, Ef, F,  Df, G,  Af, Af, Bf, Bf]
    
    for i in range (0, len(L)):
        if(mode == "Ionian"):
            L[i] = Ionian[L[i] % 12] + math.floor(L[i]/12) * 12
        elif(mode == "Dorian"):
            L[i] = Dorian[(L[i] % 12)] + math.floor(L[i]/12) * 12
        elif(mode == "Phrygian"):
            L[i] = Phrygian[L[i] % 12] + math.floor(L[i]/12) * 12
        elif(mode == "Lydian"):
            L[i] = Lydian[L[i] % 12] + math.floor(L[i]/12) * 12
        elif(mode == "Mixolydian"):
            L[i] = Mixolydian[L[i] % 12] + math.floor(L[i]/12) * 12
        elif(mode == "Aeolian"):
            L[i] = Aeolian[L[i] % 12] + math.floor(L[i]/12) * 12



img = cv2.imread(sys.argv[1])
img = cv2.resize(img, (10, 10))

r = []
g = []
b = []
for i in img:
    for j in i:
        r.append(j[0])         
        g.append(j[1])          
        b.append(j[2])          

R = []
G = []
B = []
compress(r, R, 20)
compress(g, G, 20)
compress(b, B, 20)

print("length after 1st compression")
print("---")
print(len(R))
print(len(G))
print(len(B))
print("---\n")


shiftRange(R, "High")
shiftRange(G, "Mid")
shiftRange(B, "Bass")

l = 0
s = 0
hlsImg = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
for i in hlsImg:
    for j in i:
        l = l + j[1]
        s = s + j[2]
l = l / 100
s = s / 100
print("l = ", l)
print("s = ", s)
mode = ""
if s < 100:
    if l < 255/3:
        mode = "Aeolian"
    elif l < 255*2/3:
        mode = "Mixolydian"
    else:
        mode = "Lydian"
else:
    if l < 255/3:
        mode = "Dorian"
    elif l < 255*2/3:
        mode = "Phrygian"
    else:
        mode = "Ionian"
print("mode= ", mode)
shiftMode(R, mode)
shiftMode(G, mode)
shiftMode(B, mode)

RR = []
compress(R, RR, 4)
GG = []
compress(G, GG, 4)
BB = []
compress(B, BB, 4)

print("length after 2nd compression")
print("---")
print(len(RR))
print(len(GG))
print(len(BB))
print("---\n")

bpm = (l + s) / 2
timeSlice = math.floor(250 / (bpm/60))
print("bpm = ", bpm)
print("timeSlice", timeSlice)

fR = open('R.txt', 'w')
fG = open('G.txt', 'w')
fB = open('B.txt', 'w')
sumR = 0
sumG = 0
sumB = 0


for i in RR:
    time = random.randrange(timeSlice, timeSlice*4, timeSlice)
    sumR = sumR + time
    fR.write(str(time) + " R " + str(i) + ";\n")
for i in GG:
    time = random.randrange(timeSlice, timeSlice*4, timeSlice)
    sumG = sumG + time
    fG.write(str(time) + " G " + str(i) + ";\n")
for i in BB:
    time = random.randrange(timeSlice, timeSlice*4, timeSlice)
    sumB = sumB + time
    fB.write(str(time) + " B " + str(i) + ";\n")

print("time")
print("---")
print(sumR/1000)
print(sumG/1000)
print(sumB/1000)
print("---")
