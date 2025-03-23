import cmd
import readline
import threading
import sys
import socket


responces = {}
current_id = 1


def msgclient(reciever, cmdclient):
        global responces
        while message := reciever.recv(2048):
            message = message.rstrip().decode()
            message = message.split(' ', 1)
            id = message[0]
            message = message[1]

            if id == "0":
                print("\n" + message + "\n" + cmdclient.prompt + readline.get_line_buffer(), end="", flush=True)
            else:
                responces[int(id)] = message
                print("\n" + message + "\n" + cmdclient.prompt + readline.get_line_buffer(), end="", flush=True)#


def msgsend(sender, message, await_responce=False):
    id = 0
    if await_responce:
        global current_id
        id = current_id
        current_id += 1
        if current_id == 1000000:
            current_id = 0
    sender.sendall((str(id) + " " + message + "\n").encode())

def awaitResponce():
    global responces, current_id
    id = current_id - 1
    while True:
        if id in responces:
            responce = responces[id]
            del responces[id]
            return responce


class client(cmd.Cmd):
    prompt = '> '
    
    def __init__(self, sender):
        self.sender = sender
        super().__init__()

    def do_who(self, args):
        msgsend(self.sender, "who " + args)
    
    def do_cows(self, args):
        msgsend(self.sender, "cows " + args)

    def do_quit(self, args):
        msgsend(self.sender, "quit " + args)

    def do_login(self, args):
        msgsend(self.sender, "login " + args)

    def do_yield(self, args):
        msgsend(self.sender, "yield " + args)

    def do_say(self, args):
        msgsend(self.sender, "say " + args)

    def complete_say(self, text, line, begidx, endidx):
        msgsend(self.sender, "who", True)
        cows = awaitResponce().split()
        
        beginning = (line + ".").split()[-1][:-1]
        completion_dict = [cow for cow in cows if cow.startswith(beginning)]
        return completion_dict
    
    def complete_login(self, text, line, begidx, endidx):
        msgsend(self.sender, "cows", True)
        cows = awaitResponce().split()
        
        beginning = (line + ".").split()[-1][:-1]
        completion_dict = [cow for cow in cows if cow.startswith(beginning)]
        return completion_dict


if __name__ == "__main__":
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        clientcmd = client(s)

        msgthread = threading.Thread(target=msgclient, args=(s, clientcmd))
        msgthread.start()
        clientcmd.cmdloop()
        msgthread.join()