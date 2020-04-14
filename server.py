import socket
import time
import select
import random

QnA = {"Q" + str(i): i for i in range(1, 101)}  # using dictionary comprehension
# Q1:1 ; Q2:2 ; Q3:3 ... Q100:100 ; answer to Qn is n
clients = []  # list to store the connection objects of the clients
scores = [0, 0, 0]  # maintain the score of each player


# create a socket to establish connection between client and server
def create_socket():
    try:
        global host
        global port
        global server
        host = ""
        print("Enter port to host the game.")
        port = input()
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global server
        print("Binding the port: " + str(port))

        server.bind((host, int(port)))
        server.listen(5)  # number of connections allowed before refusing new ones

    except socket.error as msg:
        print("Socket binding error occurred: " + str(msg))


# Handling connections from multiple players and saving to a list
def accepting_connections():
    """for client in clients:
        client.close()  # closing previous connections when server is restarted

    del clients[:]  # delete all entries in the list"""
    count = 0

    while True:
        client, address = server.accept()
        server.setblocking(True)  # prevents timeout
        count += 1  # increasing the count of number of connections
        clients.append(client)  # adding the connection object to the list

        if count < 3:
            print("Connection established with client {} with address {}".format(count, address[0]))
            client.send(str.encode(
                "There are a total of 100 questions.\nPress any alphabet key to buzz.\n+1 if answer is "
                "correct or a penalty of -0.5 for a wrong one.\nFirst player to reach 5 points wins.\nBest of luck!"))
            time.sleep(1)  # just for beautification purposes
            client.send(str.encode("You are player : " + str(count)))
            time.sleep(1)  # give little pauses to the player
            client.send(str.encode("Welcome to the quiz!"))

        else:  # all have been connected; triggered the moment player3 connects; thus game starts
            print("Connection established with client {} with address {}".format(count, address[0]))
            client.send(str.encode(
                "There are a total of 100 questions.\nPress any alphabet key to buzz.\n+1 if answer is "
                "correct or a penalty of -0.5 for a wrong one.\nFirst player to reach 5 points wins.\nBest of luck!"))
            print("All three players connected. Game starts.")
            time.sleep(1)
            client.send(str.encode("You are player : " + str(count)))
            time.sleep(1)
            client.send(str.encode("Welcome to the quiz!"))

            quiz()
            break  # don't accept any more connections


def quiz():
    for i in range(len(QnA)):  # iterate through the dict
        question = random.choice(list(QnA.keys()))  # choosing a random question
        answer = QnA[question]  # corresponding answer to the question
        QnA.pop(question)  # remove that question (and subsequently answer) from the dict to ensure no repetitions
        for client in clients:
            time.sleep(0.1)
            client.send(str.encode("Your question is : " + question + "\n" + "Press any alphanumeric key to buzz."))
            # send question to each player
        key_press = select.select(clients, [], [], 10)  # 10 is the timeout
        # key_press is a tuple of lists
        # Reading reference: https://pymotw.com/3/select/

        if len(key_press[0]) > 0:  # if somebody has pressed the buzzer
            who_buzzed = key_press[0][0]  # the player who buzzed the earliest
            buzz = str(who_buzzed.recv(1024), "utf-8")  # receiving the buzz value
            key_press = ()
            for client in clients:
                if client != who_buzzed:  # send message to other players
                    client.send(str.encode(
                        "Sorry, player " + str(clients.index(who_buzzed) + 1) + " has pressed the buzzer."))

            for client in range(len(clients)):
                if clients[client] == who_buzzed:
                    who_buzzed_index = client  # t is index of player who buzzed

            if buzz.isalnum():
                # implement press any key to buzz, okay?
                who_buzzed.send(str.encode("You have buzzed, please answer."))
                answer_keypress = select.select(clients, [], [], 10)

                if len(answer_keypress[0]) > 0:
                    attempt = str(who_buzzed.recv(1024), "utf-8")
                    if str(attempt) == str(answer):
                        scores[who_buzzed_index] = scores[who_buzzed_index] + 1
                        who_buzzed.send(str.encode("Correct answer, You get 1 point"))
                        if scores[who_buzzed_index] == 5:
                            for client in clients:
                                client.send(str.encode("end game"))
                                time.sleep(1)
                            break
                    else:
                        who_buzzed.send(str.encode("Wrong answer :(, you get a penalty."))
                        scores[who_buzzed_index] = scores[who_buzzed_index] - 0.5
                        time.sleep(1)
                else:
                    who_buzzed.send(str.encode("Your 10 seconds to answer have elapsed." + "\n" + "You get a penalty "
                                                                                                  "as you did not "
                                                                                                  "answer."))
                    scores[who_buzzed_index] = scores[who_buzzed_index] - 0.5

            '''elif buzz == str(answer):  # answer before buzzing
                who_buzzed.send(str.encode("You didn't press the buzzer before answering."))
                time.sleep(1)'''

        else:
            for client in clients:
                client.send(str.encode("Moving on to the next question as nobody buzzed."))


def main():
    create_socket()
    bind_socket()
    accepting_connections()
    score_winner = 0  # marks of person who won
    index_winner = 0  # index of person who won

    for i in range(len(clients)):
        if scores[i] > score_winner:
            index_winner = i
            score_winner = scores[i]

    for client in clients:
        if clients.index(client) != index_winner:
            client.send(
                str.encode("Player " + str(index_winner) + "has won with " + str(score_winner) + " points."))
        else:
            client.send(str.encode("You are the winner with " + str(score_winner) + " points. Congratulations!"))


main()
