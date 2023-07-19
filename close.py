import serial.tools.list_ports
import threading
import time

def check_presence(correct_port, interval=0.1):
    while True:
        openPorts = serial.tools.list_ports.comports()

        if arduino_port not in myports:
            print ("Arduino has been disconnected!")
            break

        time.sleep(interval)

