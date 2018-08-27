#!/usr/bin/python2.7
import random

def generateNumber():
    # create phoneID
    A = str(random.randint(1,999))
    B = str(random.randint(1,999))
    C = str(random.randint(1,999))
    while len(A) < 3:
        A += "0" 
    while len(B) < 3:
        B += "0"
    while len(C) < 3:
        C += "0"
    phoneID = A + B + C
    return phoneID

def generateRandomCall():
    # Incoming/Outgoing
    direction = ['incoming','outgoing']
    d = random.randint(0,1)
    #length of call
    length = random.randint(0,20)
    di = {"phone":generateNumber(),"direction":direction[d], "length":length}
    return di

def generateFriendlyCall(friends):
    # Incoming/Outgoing
    direction = ['incoming','outgoing']
    d = random.randint(0,1)
    #length of call
    length = random.randint(0,50)
    call = random.randint(0, len(friends)-1)
    di = {"phone":friends[call],"direction":direction[d], "length":length}
    return di
    
def generateFriendly(maxF):
    # goes to 'friendly' numbers
    # friendly number is a number called multiple times
    friendly = []
    for x in range (0,random.randint(1,maxF)):
       friendly.append(generateNumber()) 
    return friendly

if __name__ == "__main__":
    # Generate ID
    ID = 'USER_'+generateNumber() + '.txt'
    with open(ID,'a') as f:
        # generate friends
        maxF = random.randint(4,10)
        friends = generateFriendly(maxF) 
        # choose between friendly/random
        howFriendly = random.randint(4,9)
        for x in range(0,random.randint(100,1000)):
            y = random.randint(1,10)
            if y < howFriendly:
                f.write(str(generateFriendlyCall(friends))+ '\n')
            else:
                f.write(str(generateRandomCall()) + '\n')
