import socket
import time
import select
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Enter port of the server.")
port = input()
client.connect(('localhost', int(port)))  # connect to server

intro_msg = str(client.recv(1024), "utf-8")  # intro message
print(intro_msg)
questions = 100
current_question = 0
player_msg = str(client.recv(1024), "utf-8")  # You are player: n
print(player_msg)
welcome_msg = str(client.recv(1024), "utf-8")  # Welcome to the quiz!
print(welcome_msg)

while current_question < questions:  # index of question running < total number of questions

    data = str(client.recv(1024), "utf-8")  # question received OR moving on message OR to end the game
    if data == "end game":
        break  # end of game
    print(data)
    read, write, error = select.select([sys.stdin, client], [], [], 10)  # 10 is the timeout
    # check if stdin has some data
    # read = [<_io.TextIOWrapper name='<stdin>' mode='r' encoding='UTF-8'>] if something is input
    # sys.stdin = [<_io.TextIOWrapper name='<stdin>' mode='r' encoding='UTF-8'>] always
    # write and error are empty

    if len(read) > 0:
        if read[0] == sys.stdin:  # somebody buzzed
            # print("Value of c[0]: {}".format(c[0]))
            # print("Value of sys.stdin: {}".format(sys.stdin))
            buzz = input()  # input for buzz value
            client.send(str.encode(buzz))
        else:  # no buzzers
            next_question = str(read[0].recv(1024), "utf-8")  # next question
            print(next_question)
            current_question = current_question + 1
            continue

    a_t_q = str(client.recv(1024), "utf-8")  # message: "answer the question"
    print(a_t_q)
    if a_t_q == 'You have buzzed, please answer.':
        read1, write1, error1 = select.select([sys.stdin, client], [], [], 10)
        if len(read1) > 0:
            if read1[0] == sys.stdin:
                attempt = input()
                time.sleep(1)
                client.send(str.encode(attempt))
                current_question = current_question + 1
                result = str(client.recv(1024), "utf-8")  # correct answer, you get 1 point
                print(result)
            else:
                elapsed = str(client.recv(1024), "utf-8")  # 10 seconds to answer (after buzz) have elapsed
                print(elapsed)

unknown1 = str(client.recv(1024), "utf-8")
print(unknown1)
