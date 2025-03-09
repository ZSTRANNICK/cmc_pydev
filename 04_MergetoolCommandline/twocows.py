from cowsay import cowsay
import cmd
import shlex

def isFlag(s :str):
    """"""
    if not s or len(s) < 2 or s[0] != '-':
        return False
    elif s[1] == '-':
        return [s[2:]]
    else:
        return [i for i in s[1:]]

def getArgs(args, n :int, flagname=''):
    """"""
    errormsg = f"error: not enough arguments for flag {flagname}"
    if len(args) >= n:
        return args[:n]
    print(errormsg)
    return False


def argParse(args, posargs_n, flags, defaults):
    """"""
    posargs = []

    i = 0
    while i < len(args):
        flag = isFlag(args[i])
        if flag:
            for f in flag:
                if f in flags.keys():
                    flagArgs = getArgs(args[i + 1:], flags[f], f)
                    if flagArgs != None:
                        i += flags[f]
                        defaults[f] = flagArgs 
                    else:
                        print(f"error: not enough arguments for flag {f}")
                        return None
                else:
                    print(f"error: no such flag {f}")
        else:
            posargs.append(args[i])
        i += 1

    if len(posargs) < posargs_n:
        print("error: not enough arguments")
        return None
    elif len(posargs) > posargs_n:
        print("error: too many arguments")
        return None
    return (posargs, defaults)
 

class cowsay(cmd.Cmd):
    prompt = 'cowsay > '

    def do_cowsay(self, args):
        """Generates an ASCII image of a cow saying the given text"""
        args = shlex.split(args) 

        args = argParse(args, 2, {'e': 1, 'E': 1, 'f': 1, 'F': 1, 't': 1, 'T': 1}, {'e': 'oo', 'E': 'oo', 'f': 'default', 'F': 'default', 't': ' ', 'T': ' '})

        if args == None:
            return

        posargs, flagargs = args
        #print cows

       
    def do_EOF(self, _):
        print()
        exit()

    def do_q(self, _):
        print()
        exit()

if __name__ == '__main__':
    cowsay().cmdloop()
