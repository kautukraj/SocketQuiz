from socket import *

serverName = 'localhost'
serverPort = 1025
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
name = input('Enter player name: ')
clientSocket.send(bytes(name, "utf-8"))

while 1:
    question = (clientSocket.recv(1024)).decode()
    print("Question: ", question)
    attempt = input('Input your answer: ')
    clientSocket.send(bytes(attempt, "utf-8"))
# clientSocket.close()

