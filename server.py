from socket import *
import random
import sys
import time
# please use functions :(
serverPort = 1025
serverSocket = socket(AF_INET, SOCK_STREAM)  # create a new socket using the given address family and socket type
# SOCK_STREAM = TCP socket
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(3)
print("Server is setup")
QnA = {"Q1": "A1", "Q2": "A2"}
connections = []
addresses = []
names = []
score = {}

for i in range(0, 1):
    connectionSocket, address = serverSocket.accept()
    name = (connectionSocket.recv(1024)).decode()
    serverSocket.setblocking(True)
    connections.append(connectionSocket)
    names.append(name)
    score[name] = 0
    print("Connected to ", address, name)

while len(QnA) != 0:
    question = random.choice(list(QnA.keys()))
    answer = QnA[question]
    QnA.pop(question)
    print("Your question is: ", question)

    for i in range(0, 1):
        connections[i].send(bytes(question, "utf-8"))

    # find out who buzzed
    buzzed = names[0]

    for i in range(10, 0, -1):
        sys.stdout.write(str(i) + ' ')
        sys.stdout.flush()
        time.sleep(1)

    # do you have an answer?
    start_time = time.time()
    attempt = (connections[0].recv(1024)).decode()
    time_elapsed = time.time() - start_time
    if time_elapsed > 10 or attempt is None:
        continue
    else:
        print("{} gives answer {}".format(buzzed, attempt))

        if attempt == answer:  # ignore case in matching
            score[buzzed] = score[buzzed] + 1
        else:
            score[buzzed] = score[buzzed] - 0.5

    '''if answerGiven:
        attempt = (connections[i].recv(1024)).decode()
        print("{} gives answer {}".format(buzzed, attempt))

        if attempt == answer:  # ignore case in matching
            score[buzzed] = score[buzzed] + 1
        else:
            score[buzzed] = score[buzzed] - 0.5

    for i in range(0, 2):
        if score[names[i]] > 0.5:
            print("{} is the winner".format((names[i])))
            print("Game is closing now...")
            connections[i].close()
            serverSocket.close()
            sys.exit()'''

print("Ran out of questions, game closing.")
for i in range(0, 1):
    connections[i].close()
serverSocket.close()
sys.exit()
