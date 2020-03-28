from socket import *
import random
import sys
import time
# please use functions :(
serverPort = 1025
serverSocket = socket(AF_INET, SOCK_STREAM)  # create a new socket using the given address family and socket type
# SOCK_STREAM = TCP socket and AF_INET = IPv4
serverSocket.bind(('localhost', serverPort))  # bind the server to given port and hostname
serverSocket.listen(3)  # can connect to a maximum of three clients
print("Server is setup")
QnA = {"Q1": "A1", "Q2": "A2"}  # dictionary of questions(keys) and answers(values)
connections = []  # list to store the client sockets
addresses = []  # list to store client addresses
names = []  # list to store client names (given as user input)
score = {}  # dictionary to store scores of all participants
no_of_players = 2  # will change this to 3 later

for i in range(0, no_of_players):
    connectionSocket, address = serverSocket.accept()  # accept client connections
    name = (connectionSocket.recv(1024)).decode()  # receive client names
    serverSocket.setblocking(True)  # IDK what this does exactly
    connections.append(connectionSocket)
    names.append(name)
    score[name] = 0  # initialize score of each to 0
    print("Connected to ", address, name)

while len(QnA) != 0:
    question = random.choice(list(QnA.keys()))  # choosing a random question
    answer = QnA[question]  # corresponding answer
    QnA.pop(question)  # remove that question(and subsequently answer) from the dict to ensure no repetitions
    print("Your question is: ", question)

    for client in connections:
        client.send(bytes(question, "utf-8"))  # send question to all the players(clients)
        client.send(bytes("Buzz by pressing any key", "utf-8"))

    who_buzzed = None  # store index of buzzing player
    buzz = None  # truth value of buzzer, on or off. None = off; anything else = on
    start_time = time.time()

    while who_buzzed is None and time.time() - start_time < 10:  # while nobody has buzzed and 10 seconds have not
        # elapsed
        for client in connections:
            try:
                buzz = client.recv(1024).decode()
            except:
                buzz = None
            if buzz is not None:
                who_buzzed = client
                break

    # countdown timer
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
