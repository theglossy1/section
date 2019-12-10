"""
Read a Cisco configuration file and interpret it the same as:
  show command output | section <pattern-to-match>

This uses Python's "re" module adapted to Cisco's regex parser... it is not a
perfect match. Be particularly careful when using the _ character, though it
generally works fine.
"""

import sys, os, re, argparse

parser = argparse.ArgumentParser(
    description="Read a Cisco configuration file and interpret it the same as:\n  show command output | section <pattern-to-match>\n\nWorks great for displaying chunks of Python programs too!",
    usage='%(prog)s [options] "pattern to match" [filename]', formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument("search_string", metavar="pattern-to-match", help="pattern to match; quotes are required if pattern contains spaces; supports regex")
parser.add_argument("file", metavar='filename', nargs="?", type=argparse.FileType('r'), default=sys.stdin, help="file to read from; if not specified, read from STDIN")
parser.add_argument("-i","--ignore-case", action="store_true", dest="ignore_case", help="ignore case distinctions")
parser.add_argument("-m","--max-count", metavar="NUM", dest="max_count", type=int, default=0, help="stop after NUM matches")
parser.add_argument("-n","--line-number", action="store_true", dest="print_line_num", help="print line number with output lines")
parser.add_argument("-b","--add-blank", action="store_true", dest="blank_line", help="add a blank line between matched sections for readability")
parser.add_argument("-v","--verbose", action="store_true", dest="verbose", help="show pattern that will be matched")

args = parser.parse_args()

# convert argparse variables to globals
globals().update(vars(args))

def ctrlc(type,*args):
    "Ctrl+C handler"
    if type==KeyboardInterrupt:
        print("!!! Terminated by ^C !!!")
        sys.exit()
    else:
        sys.__excepthook__(type,*args)

sys.excepthook = ctrlc

def printout(line_to_print):
    try:
        if print_line_num: print(f'{i+1}:{line_to_print}')
        else: print(line_to_print)
    except BrokenPipeError:
        sys.exit(0)

try:
    file_list = list(file)
except UnicodeDecodeError:
    print(f"'{filepath}' appears to be a binary file. Only text files are supported.")
    sys.exit(1)

# convert the _ to Cisco match methodology:
# see https://www.cisco.com/en/US/products/sw/iosswrel/ps1835/products_configuration_guide_chapter09186a00803479f1.html
search_string = search_string.replace("_","([_\)\({},\s]|^|$)")

if verbose:
    print(f"! Interpreted search string: {search_string}\n")

i = 0
count = 0
while i < len(file_list):
    line = file_list[i].rstrip()
    try:
        if ignore_case: matched = re.search(rf'{search_string}',line,re.I)
        else: matched = re.search(rf'{search_string}',line)
    except re.error as err:
        print(search_string)
        error_pos = re.search(r'([0-9]+)$',str(err)).group(0)
        print(" "*int(error_pos) + "^")
        print(f"Error compiling regular expression: {err}")
        sys.exit(1)

    if matched is not None and (max_count == 0 or count < max_count):
        matched_line = line
        if max_count > 0: count += 1
        printout(matched_line)
        matched_line_nonwhitespace_index = re.search(r'\S',matched_line)
        while True:
            i += 1
            try:
                current_line = file_list[i].rstrip()
            except IndexError:
                # end-of-file was reached
                sys.exit(0)
            current_line_nonwhitespace_index = re.search(r'\S',current_line)
            if current_line_nonwhitespace_index is not None and matched_line_nonwhitespace_index is not None:
                if current_line_nonwhitespace_index.start() > matched_line_nonwhitespace_index.start():
                    printout(current_line)
                else:
                    break
        if blank_line: print()
        continue
    i += 1
