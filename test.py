from communications import OldPortConnection
import time
import random

port = OldPortConnection()
print(port.connectToPort())
file = open("output.txt", "w")
time.sleep(1)
#port.sendHeartbeat()
#time.sleep(0.5)

def generateString():
    starterString = "<d,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,:,"
    values = [1, -1]

    for i in range(1, 16):
        if (i == 15):
            multiplier = random.choice(values)
            starterString += "{}".format(i*multiplier)
            continue

        multiplier = random.choice(values)
        starterString += "{},".format(i*multiplier)

    starterString += ">"
    return starterString

arduino = port.getArduino()

while True:

    if (port.arduino.in_waiting > 0):
        response = arduino.readline().decode('utf-8').rstrip('\n')
        print (response + "\n")
        file.write(response + "\n")
        # port.printLine()

    stringRequest = generateString()
    print (stringRequest + "\n")
    port.arduino.write(stringRequest.encode('utf-8'))
    file.write(stringRequest + "\n")

    #x = input("Enter a message: ")
    #port.arduino.write(x.encode('utf-8'))
    time.sleep(0.25)

