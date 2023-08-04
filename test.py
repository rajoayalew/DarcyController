from communications import PortConnection
import serial
import time

port = PortConnection()
print(port.connectToPort())
time.sleep(1)
#port.sendHeartbeat()
#time.sleep(0.5)

"""
arduino = port.getArduino()

def write_read(x):
    arduino.write(bytes(x,  'utf-8'))
    time.sleep(0.05)
    data = arduino.readline().decode('utf-8').rstrip('\n')
    return  data
"""

arduino = port.getArduino()

while True:

    x = input("Enter a message: ")
    port.arduino.write(x.encode('utf-8'))
    #print (port.arduino.in_waiting)
    time.sleep(0.5)

    if (port.arduino.in_waiting > 0):
        print (arduino.readline().decode('utf-8').rstrip('\n'))
        # port.printLine()

