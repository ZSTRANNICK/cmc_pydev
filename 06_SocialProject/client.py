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


def msgsend(sender, message):
    global current_id
    sender.sendall((str(current_id) + " " + message + "\n").encode())
    current_id += 1



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