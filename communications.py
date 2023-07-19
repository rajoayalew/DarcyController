import serial.tools.list_ports
import time
import threading

class PortConnection():
    def __init__(self):
        self.portList = []
        self.arduino = None
        self.portName = None

    def updatePortList(self):
        ports = serial.tools.list_ports.comports()
        portsList = []

        for port in ports:
            port = str(port)
            port = port.split(" ")[0]
            portsList.append(port)

        self.portList = portsList

    def connectionStatus(self):
        self.updatePortList()

        portList = self.getPortList()

        if (len(portList) == 0):
            return 0
        elif (len(portList) == 1):
            return 1
        elif (len(portList) > 1):
            return 2
        else:
            return 3

    def connectToPort(self):
        if (self.connectionStatus() == 1):
            connectedPort = self.portList[0]

            try:
                self.arduino = serial.Serial(connectedPort, 9600, timeout=10)
                self.portName = connectedPort
                return ("Succesffuly connected to Arduino on port " + connectedPort)
            except (FileNotFoundError):
                return ("Failed to connect to Arduino as the selected port doesn't exist.")
            except:
                return ("Unknown error.")
        elif (self.connectionStatus == 0):
            return ("There are no open ports to connect to.")
        elif (self.connectionStatus > 1):
            return ("There are more than one open port. Make sure you only have one Arduino plugged in")
        elif (self.connectionStatus == 3):
            return ("You really fucked up to get this error")

    def connectToPortCode(self):
        if (self.connectionStatus() == 1):
            connectedPort = self.portList[0]

            try:
                self.arduino = serial.Serial(connectedPort, 9600, timeout=10)
                self.portName = connectedPort
                return 0
            except (FileNotFoundError):
                return 1
            except:
                return 2
        elif (self.connectionStatus() == 0):
            return 3
        elif (self.connectionStatus() > 1):
            return 4
        elif (self.connectionStatus() == 3):
            return 5

    def printLine(self):
        if (self.connectionStatus() == 1):
            data = self.arduino.readline()
            data = data.decode('utf-8').rstrip('\n')
            print (data)
        else:
            print ("No connection")

    def getArduino(self):
        return self.arduino

    def getPortList(self):
        return self.portList

    def getPortName(self):
        return self.portName

    def getArduino(self):
        return self.arduino

    def printPortList(self):
        print (self.portList)







"""def check_presence(correct_port, interval=0.1):
    while True:
        openPorts = [str(port) for port in list(serial.tools.list_ports.comports())]

        if correct_port not in openPorts:
            print ("Arduino has been disconnected!")
            break

        time.sleep(interval)

ports = serial.tools.list_ports.comports()
portList = []

for port in ports:
    portList.append(str(port))
    #print(str(port))

if (len(portList) > 1):
    print ("There are more than one serial port connected " +
           "indicating you have more than one thing connected")

if (len(portList) == 0):
    print ("Arduino is not connected")

connectedPort = (portList[0].split(" "))[0]
arduinoPort = portList[0]

arduino = serial.Serial(connectedPort, 9600, timeout=10)

port_controller = threading.Thread(target=check_presence, args=(arduinoPort, 0.1))
port_controller.setDaemon(True)
port_controller.start()

print (arduino.name)

while True:
    data = arduino.readline()
    data = data.decode('utf-8').rstrip('\n')
    print(data)

"""
