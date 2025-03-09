import cmd
import shlex
from cowsay import cowsay, cowthink, make_bubble, list_cows, COW_PEN

def isFlag(s :str):
    """
    Check if string *s* is a flag.
    If string starts with one '-', return array of the symbols following it.
    If string starts with '--', return an array with one word.
    Otherwise returns False.
    """
    if not s or len(s) < 2 or s[0] != '-':
        return False
    elif s[1] == '-':
        return [s[2:]]
    else:
        return [i for i in s[1:]]

def getArgs(args, n :int, flagname=''):
    """
    Returns arguments for flag or False if their count is wrong.
    *args*     - array of tokens.
    *n*        - number of required arguments.
    *flagname* - name of the flag (for an error message).
    """
    errormsg = f"error: not enough arguments for flag {flagname}"
    if len(args) >= n:
        return args[:n]
    print(errormsg)
    return False


def argParse(args, posargs_n, flags, defaults={}):
    """
    Parses arguments for a command.
    *args*      - array of tokens
    *posargs_n* - number of positional tokens required
    *flags*     - dictionary with keys as flags (strings) and values
                  as number of required arguments for a flag
    *defaults*  - default values for flags' arguments
    """
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


def cow_concat(cows):
    cows_widths = []
    cows_maxwidths = []
    cows_lines_count = []
    cows_maxlines_count = 0
    cows_lines = []

    for cow in cows:
        cow_widths = []
        cow_maxwidth = 0
        cow_lines_count = 0
        lines = cow.split('\n')

        for line in lines:
            cow_lines_count += 1
            cow_widths.append(len(line))
            if cow_maxwidth < len(line):
                cow_maxwidth = len(line)
        
        cows_widths.append(cow_widths)
        cows_maxwidths.append(cow_maxwidth)
        cows_lines.append(lines)
        cows_lines_count.append(cow_lines_count)
        if cows_maxlines_count < cow_lines_count:
            cows_maxlines_count = cow_lines_count

    result = ""
    for i in range(cows_maxlines_count, 0, -1):
        for j in range(len(cows_lines_count)):
            if cows_lines_count[j] >= i:
                result += cows_lines[j][0] + (cows_maxwidths[j] - cows_widths[j][0] + 1) * ' '
                cows_lines[j].pop(0)
                cows_widths[j].pop(0)
            else:
                result += (cows_maxwidths[j] + 1) * ' '
        result += '\n'
    
    return result


class twocows(cmd.Cmd):
    prompt = 'cowsay > '

    def do_cowsay(self, args):
        """
        Generates an ASCII image of two cows saying the given text
        message1           - message of the first cow 
        message2           - message of the seconds cow
        -e [eyes_string]   - eyes of the first cow
        -E [eyes_string]   - eyes of the second cow
        -f [cow_name]      - name of the first cow 
        -F [cow_name]      - name of the second cow
        -t [tongue_string] - tongue of the first cow
        -T [tongue_string] - tongue of the second cow
        """

        args = shlex.split(args)

        args = argParse(args, 2, {'e': 1, 'E': 1, 'f': 1, 'F': 1, 't': 1, 'T': 1},
                        {'e': ['oo'], 'E': ['oo'], 'f': ['default'], 'F': ['default'], 't': ['  '], 'T': ['  ']})

        if args == None:
            return

        posargs, flagargs = args
        print(cow_concat([cowsay(posargs[0], cow=flagargs['f'][0], eyes=flagargs['e'][0], tongue=flagargs['t'][0]),
                          cowsay(posargs[1], cow=flagargs['F'][0], eyes=flagargs['E'][0], tongue=flagargs['T'][0])]))


    def do_cowthink(self, args):
        """
        Generates an ASCII image of a two cows thinking the given text
        message1           - message of the first cow 
        message2           - message of the seconds cow
        -e [eyes_string]   - eyes of the first cow
        -E [eyes_string]   - eyes of the second cow
        -f [cow_name]      - name of the first cow 
        -F [cow_name]      - name of the second cow
        -t [tongue_string] - tongue of the first cow
        -T [tongue_string] - tongue of the second cow
        """

        args = shlex.split(args) 

        args = argParse(args, 2, {'e': 1, 'E': 1, 'f': 1, 'F': 1, 't': 1, 'T': 1},
                        {'e': ['oo'], 'E': ['oo'], 'f': ['default'], 'F': ['default'], 't': ['  '], 'T': ['  ']})

        if args == None:
            return

        posargs, flagargs = args
        print(cow_concat([cowthink(posargs[0], cow=flagargs['f'][0], eyes=flagargs['e'][0], tongue=flagargs['t'][0]),
                          cowthink(posargs[1], cow=flagargs['F'][0], eyes=flagargs['E'][0], tongue=flagargs['T'][0])]))


    def do_list_cows(self, args):
        """Lists all cow file names in the given directory"""
        if args:
            args = shlex.split(args)
            if len(args) > 1:
                print("error: too many arguments")
                return
            args = args[0]
        else:
            args = COW_PEN
        
        cows = list_cows(args)
        for cow in cows:
            print(cow)


    def do_make_bubble(self, args):
        """
        Wraps text in a bubble
        text                - text to wrap
        --width [width_int] - max width of the bubble
        """
        args = shlex.split(args)
        args = argParse(args, 1, {'width': 1}, {'width': ['40']})
        if args == None:
            return
        posargs, flagargs = args
        print(make_bubble(posargs[0], width=int(flagargs['width'][0])))

       
    def do_EOF(self, _):
        """Exit the program"""
        print()
        exit()

    def do_q(self, _):
        """Exit the program"""
        print()
        exit()

if __name__ == '__main__':
    twocows().cmdloop()
