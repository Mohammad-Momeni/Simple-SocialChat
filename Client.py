from socket import *
from threading import Thread
import os
import time

def getOnlineUsers():
    serverName = 'localhost'
    serverPort = 12000
    UDPSocket = socket(AF_INET, SOCK_DGRAM)
    UDPSocket.sendto('users'.encode(), (serverName, serverPort))
    users, addr = UDPSocket.recvfrom(1024)
    users = users.decode().strip()
    if users == '':
        print('No online users')
    else:
        print(users)
    UDPSocket.close()

def getInput(message, validInputs):
    while True:
        try:
            action = int(input(message))
            if action not in validInputs:
                print('Invalid input')
                continue
            break
        except:
            print('Invalid input')
            continue
    return action

def printMessages():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    for message in messages:
        print(message)
    print(state)
    return

def addMessage(message):
    if message[1] == 'public':
        if message[0].split(':')[0] == username:
            messages.append('You:' + message[0].split(':')[1] + '\t\ttime: ' + message[0].split(':')[2])
        else:
            messages.append(message[0].split(':')[0] + ':' + message[0].split(':')[1] + '\t\ttime: ' + message[0].split(':')[2])
    elif message[1] == 'private':
        if message[0].split(':')[0] == username:
            messages.append('You to ' + message[0].split(':')[1] + ': ' + message[0].split(':')[2] + '\t\ttime: ' + message[0].split(':')[3])
        else:
            messages.append('Private message from ' + message[0].split(':')[0] + ': ' + message[0].split(':')[2] + '\t\ttime: ' + message[0].split(':')[3])
    elif message[1] == 'group':
        if message[0].split(':')[0] == username:
            messages.append('You to group: ' + message[0].split(':')[1] + '\t\ttime: ' + message[0].split(':')[2])
        else:
            messages.append('Group message from ' + message[0].split(':')[0] + ': ' + message[0].split(':')[1] + '\t\ttime: ' + message[0].split(':')[2])
def getMessages():
    while True:
        try:
            message = clientSocket.recv(1024)
            message = message.decode().split('&')
            if message[1] == 'exit':
                return
            elif message[1] == 'userBusy':
                print('User is busy')
                continue
            elif message[1] == 'userNotFound':
                print('User not found')
                continue
            addMessage(message)
            printMessages()
        except:
            pass

state = ''
messages = []
username = ''
status = ''
while True:
    action = getInput('Enter 1 to connect to server, 2 to get online users, 3 to exit:\n', [1, 2, 3])
    if action == 3:
        break
    elif action == 2:
        getOnlineUsers()
    elif action == 1:
        serverName = 'localhost'
        serverPort = 12000
        clientSocket = socket(AF_INET, SOCK_STREAM)
        username = input('Enter your username:\n')
        password = input('Enter your password:\n')
        action = getInput('Choose status:\n1)Available\n2)Busy\n', [1, 2])
        if action == 1:
            status = 'available'
        else:
            status = 'busy'
        credentials = username + '\0' + password + '\0' + status
        try:
            clientSocket.connect((serverName, serverPort))
            clientSocket.send(credentials.encode())
            try:
                message = clientSocket.recv(1024)
                message = message.decode()
                if message == '&wrongPassword':
                    print('Wrong Password')
                    clientSocket.close()
                    continue
                elif message == '&online':
                    print('Username is already Online')
                    clientSocket.close()
                    continue
                else:
                    if message != '&accepted':
                        message = message.split('\0')
                        for i in range(len(message)):
                            addMessage(message[i].split('&'))
                        if os.name == 'nt':
                            os.system('cls')
                        else:
                            os.system('clear')
                        for message in messages:
                            print(message)
            except:
                print('there was an error connecting to the server')
                continue
            t = Thread(target=getMessages)
            t.start()
            while True:
                if status == 'available':
                    state = 'Enter 1 to send message, 2 to get online users, 3 to change your status, 4 to close connection:'
                    action = getInput(state + '\n', [1, 2, 3, 4])
                else:
                    state = 'Enter 1 to get online users, 2 to change your status, 3 to close connection:'
                    action = getInput(state + '\n', [1, 2, 3])
                    action += 1
                if action == 4:
                    clientSocket.send('&exit'.encode())
                    break
                elif action == 3:
                    action = getInput('Choose status:\n1)Available\n2)Busy\n', [1, 2])
                    if action == 1:
                        status = '&available'
                    else:
                        status = '&busy'
                    clientSocket.send(status.encode())
                    status = status[1:]
                    continue
                elif action == 2:
                    getOnlineUsers()
                    continue
                elif action == 1:
                    state = 'Enter 1 to send to all, 2 to send to a specific user, 3 to send to a group of people:'
                    action = getInput(state + '\n', [1, 2, 3])
                    state = 'Enter message:'
                    message = input(state + '\n')
                    if action == 2:
                        state = 'Enter username:'
                        message = 'private&' + input(state + '\n') + '&' + message
                    elif action == 3:
                        state = 'Enter usernames seperated by comma:'
                        message = 'group&' + input(state + '\n') + '&' + message
                    else:
                        state = 'Do you want people who join later to see this message? Enter 1 for yes, 2 for no:'
                        action = getInput(state + '\n', [1, 2])
                        if action == 1:
                            message = 'public&' + message
                        else:
                            message = 'all&' + message
                    hour = time.localtime().tm_hour
                    if hour < 10:
                        message = message + '&' + '0' + str(hour)
                    else:
                        message = message + '&' + str(hour)
                    clientSocket.send(message.encode())
            t.join()
            clientSocket.close()
            state = ''
            messages = []
            username = ''
        except:
            print('there was an error connecting to the server')
            continue