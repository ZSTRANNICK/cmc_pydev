import argparse
from cowsay import cowsay


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


parser = argparse.ArgumentParser()

parser.add_argument("-e", default='oo', help=
"""
An eye string. This is ignored if a preset mode is given
""")

parser.add_argument("-E", default='oo', help=
"""
Same as -e, but for the second cow
""")

parser.add_argument("-f", default='default', help=
"""
Name of a cow specified in the COWPATH
""")

parser.add_argument("-F", default='default', help=
"""
Same as -f, but for the second cow
"""
)

parser.add_argument("-n", action="store_true", help=
"""
If given, text in the speech bubble will not be wrapped
"""
)

parser.add_argument("-N", action="store_true", help=
"""
Same as -n, but for the second cow
"""
)

parser.add_argument("message1", type=str, help="first message")
parser.add_argument("message2", type=str, help="first message")

args = parser.parse_args()

print(cow_concat([cowsay(args.message1, cow=args.f, eyes=args.e, wrap_text=(not args.n)),
                  cowsay(args.message2, cow=args.F, eyes=args.E, wrap_text=(not args.N))]))