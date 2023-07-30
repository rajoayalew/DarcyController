import serial.tools.list_ports
import sys

class PortConnection():
    def __init__(self):
        self.arduino = None
        self.portName = None
        self.portList = serial.tools.list_ports.comports()
        self.platform = sys.platform

    def updatePortList(self):
        self.portList = serial.tools.list_ports.comports()

    def connectToPortCode(self):
        self.updatePortList()

        for port in self.portList:
            if (self.platform == "win32"):

                if "Arduino" in port.description:
                    attemptedPort = str(port).split(" ")[0]
                    code = self.connectHelper(attemptedPort)
                    return code

            elif (self.platform == "linux"):

                if "Arduino" in port.manufacturer:
                    attemptedPort = str(port).split(" ")[0]
                    code = self.connectHelper(attemptedPort)
                    return code

            elif (self.platform == "darwin"):
                return 3
            else:
                return 4

        return 5

    def connectToPort(self):
        code = self.connectToPortCode()

        match code:
            case 0:
                return ("Succesffuly connected to Arduino on port " + self.portName)
            case 1:
                return ("Failed to connect to Arduino as selected port doesn't exist")
            case 2:
                return ("Unknown error")
            case 3:
                return ("Get off MacOS")
            case 4:
                return ("You BSD folks will get support in maybe 5 years")
            case 5:
                return ("No Arduino detected. Try unplugging and replugging Arduino into computer")

    def connectHelper(self, portName):
        try:
            self.arduino = serial.Serial(portName, 9600, timeout=10)
            self.portName = portName
            return 0
        except (FileNotFoundError):
            return 1
        except:
            return 2

    def connectionStatus(self):
        if (self.portName == None):
            return 1

        self.updatePortList()
        testList = self.getHumanPortList()

        for port in testList:
            if (self.portName in port):
                return 0

        return 1

    def printLine(self):
        if (self.connectionStatus() == 0):
            data = self.arduino.readline()
            data = data.decode('utf-8').rstrip('\n')
            print (data)
        else:
            print ("No connection")

    def getArduino(self):
        return self.arduino

    def getPlatform(self):
        return self.platform

    def getPortName(self):
        return self.portName

    def getPortList(self):
        return self.portList

    def getHumanPortList(self):
        return [str(port).split(" ")[0] for port in list(serial.tools.list_ports.comports())]

