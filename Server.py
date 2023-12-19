from socket import *
from threading import Thread
import csv
import hashlib

def messagesToString(messages):
    output = ''
    for i in range(len(messages)):
        output += messages[i]
        if i != len(messages) - 1:
            output += '\0'
    return output

def clientThread(connectionSocket, addr):
    credentials = connectionSocket.recv(1024).decode().split("\0")
    hashedPassword = hashlib.md5(credentials[1].encode("utf-8")).hexdigest()
    if credentials[0] in credentialsData.keys():
        if hashedPassword == credentialsData[credentials[0]]:
            if credentials[0] in users.keys():
                # Welcome
                pass
        else:
            connectionSocket.send('&wrongPassword'.encode())
            connectionSocket.close()
            return
    else:
        credentialsData[credentials[0]] = hashedPassword



    if credentials[0] in users.keys():
        if users[credentials[0]][0] == credentials[1]:
            if users[credentials[0]][1] == 'offline':
                users[credentials[0]][1] = 'online'
                if len(publicMessages) > 0:
                    connectionSocket.send(messagesToString(publicMessages).encode())
                else:
                    connectionSocket.send('&accepted'.encode())
                return
            connectionSocket.send(messagesToString(publicMessages).encode())
            users[credentials[0]] = connectionSocket
            return
        connectionSocket.send('&taken'.encode())
        connectionSocket.close()
        return
    else:
        if len(publicMessages) > 0:
            connectionSocket.send(messagesToString(publicMessages).encode())
        else:
            connectionSocket.send('&accepted'.encode())
    users[username] = connectionSocket
    while True:
        try:
            sentence = connectionSocket.recv(1024).decode()
            if sentence == '&exit':
                connectionSocket.send('&exit'.encode())
                break
            elif sentence[0] == '&':
                sentence = sentence[1:].split('&')
                if sentence[0] == 'public':
                    publicMessages.append(username + ': ' + sentence[1] + '&public')
                    for user in users:
                        users[user].send((username + ': ' + sentence[1] + '&public').encode())
                elif sentence[0] == 'all':
                    for user in users:
                        users[user].send((username + ': ' + sentence[1] + '&public').encode())
                else:
                    if sentence[0] in users:
                        users[sentence[0]].send((username + ': ' + sentence[1] + '&private').encode())
                        users[username].send((username + ':' + sentence[0] + ':' + sentence[1] + '&private').encode())
        except:
            break
    del users[username]
    connectionSocket.close()
    return

def usersToString():
    output = ''
    usersKeys = list(users.keys())
    for i in range(len(usersKeys)):
            output += usersKeys[i]
            if i != len(usersKeys) - 1:
                output += ', '
    return output.strip()

def getOnlineUsers():
    while True:
        message, addr = UDPServerSocket.recvfrom(1024)
        if message.decode() == 'users':
            UDPServerSocket.sendto(usersToString().encode(), addr)

with open('credentials.csv', mode='r') as infile:
    reader = csv.reader(infile)
    credentialsData = {rows[0] : rows[1] for rows in reader}

users = {}
publicMessages = []
serverName = 'localhost'
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(5)
UDPServerSocket = socket(AF_INET, SOCK_DGRAM)
UDPServerSocket.bind((serverName, serverPort))
UDPThread = Thread(target=getOnlineUsers)
UDPThread.start()
print('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept()
    t = Thread(target=clientThread, args=(connectionSocket, addr, ))
    t.start()
    