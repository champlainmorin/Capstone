# Network User Management System by Zachary Morin 
# NUMS for short.

import socket
import crypt
import threading
import os
import sys
import dill
from threading import Thread
from _thread import *

"""
Look into Linux PAM and pam_script for client side authentication.
Have two server programs, one be the GUI and one the actual server,
for headless applications.
Look into appjar for GUI interaction in Python.
"""

class NUMServer:

    # Declaring class variables.
    socketList = []
    isListening = False

    userList = [
        {"username":"test",
         "password":"test"}
    ]
    
    computerList = []

    # Starting the server.
    def __init__(self, IP, Port):
        self.IP = IP
        self.PORT = Port
        self.platform = sys.platform
        
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.IP, self.PORT))
        print("Socket bound to " + self.IP + " on port " + str(self.PORT) + ".")
        

    # Listen for request, and then perform the required service.
    def backgroundListening(self):
        self.isListening = True
        self.serverSocket.listen()
        conn, addr = self.serverSocket.accept()
        self.isListening = False
        commandRecieved = conn.recv(2048).decode() # Decodes bytes object to string.
        print("\n" + addr[0] + ":" + str(addr[1]) + " sent " + '"' + str(commandRecieved) + '"') 
        
        # Do whatever based on recieved command.
        commandList = commandRecieved.split("//")
        print(commandList)
        response = self.commandParser(commandList) # Send command to parser.
        
        conn.send(bytes(response, 'utf-8')) # Send command results back.
        self.backgroundListening() # Recur listening.
        
    # Parses commands sent to the server.
    def commandParser(self, commandList):
        
        match commandList[0]:
            case "LoginCommand":
                print("Begin Login Attempt:")
                print(commandList[1])
                testCase = commandList[1].split(":")
                for case in self.userList:
                    if case["username"] == testCase[0]:
                        if case["password"] == testCase[1]:
                            return "Login Success"
                        else:
                            return "Wrong Password"
                    else:
                        return "Wrong User"
            case "GetUsersCommand":
                if commandList[1] == "ALL":
                    return str(self.userList)
                else:
                    return "Bad Command"
                
            case "JoinDomain":
                pass 
                # Create unique computer ID here for a 
                # first time joining computer.
            case _:
                return "NoResponse"

    # The main server function.
    def main(self):
        start_new_thread(self.backgroundListening, ())
    
thisServer = NUMServer('184.171.155.80', 1900)
thisServer.main()

while (True):
    try:
        userInput = input("NUMServer>")
        
        if userInput == "clear":
            os.system("clear")
        elif userInput == "show ":
            pass
        else:
            exec(userInput)
    except KeyboardInterrupt:
        break
    except NameError: 
        pass
    except SyntaxError:
        pass
