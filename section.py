# to do: Allow multiple filenames (e.g., section "text" file1.txt file2.txt ...)
"""
Read a "sectionized" output (e.g., from "ipconfig /all" on Windows or from Cisco IOS) and interpret it the same as:
    show command output | section <pattern-to-match>

This uses Python's "re" module adapted to Cisco's regex parser... it is not a
perfect match (no pun intended). Be particularly careful when using the _ 
character, though it generally works fine.
"""

import sys, os, re, argparse

try:
    import margparse
except:
    print("Please install 'more-argparse' (available via pip)")
    exit(1)

__version__ = '1.1.2'

parser = argparse.ArgumentParser(
    description=__doc__,
    usage='%(prog)s [options] "pattern to match" [filename]', formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument("search_string", metavar="pattern-to-match", help="pattern to match; quotes are required if pattern contains space; supports regex")
parser.add_argument("files", metavar='filename', nargs="*", type=margparse.GlobbingType(argparse.FileType('r')), default=[[sys.stdin]], help="file to read from; if not specified, read from STDIN")
parser.add_argument("-i","--ignore-case", action="store_true", dest="ignore_case", help="ignore case distinctions")
parser.add_argument("-m","--max-count", metavar="NUM", dest="max_count", type=int, default=0, help="stop after NUM matches")
parser.add_argument("-n","--line-number", action="store_true", dest="print_line_num", help="print line number with output lines")
parser.add_argument("-b","--add-blank", action="store_true", dest="blank_line", help="add a blank line between matched sections for readability")
parser.add_argument("-H","--with-filename", action="store_true", dest="show_filename", help="print the filename for each match")
parser.add_argument("--no-filename", action="store_true", dest="hide_filename", help="suppress the prefixing filename on output")
parser.add_argument("-v","--verbose", action="store_true", dest="verbose", help="show pattern that will be matched")
parser.add_argument("-V","--version", action="version", version=f"%(prog)s {__version__}", help="show current version")
args = parser.parse_args()

old_file_list = args.files
files = []
for sublist in old_file_list:
    files.extend(sublist)

def ctrlc(type,*args):
    "Ctrl+C handler"
    if type==KeyboardInterrupt:
        print("!!! Terminated by ^C !!!")
        sys.exit()
    else:
        sys.__excepthook__(type,*args)

sys.excepthook = ctrlc

if len(files) > 1:
    if args.hide_filename:
        show_filename = False
    else:
        show_filename = True
else:
    if args.show_filename:
        show_filename = True
    else:
        show_filename = False

def printout(line_to_print):
    try:
        if show_filename: print(f'{file.name}:',end='')
        if args.print_line_num: print(f'{i+1}:',end='')
        print(line_to_print)
    except BrokenPipeError:
        sys.exit(0)

# convert the _ to Cisco match methodology:
# see https://www.cisco.com/en/US/products/sw/iosswrel/ps1835/products_configuration_guide_chapter09186a00803479f1.html
search_string = args.search_string.replace("_",r"([_\)\({},\s]|^|$)")

if args.verbose:
    print(f"! Interpreted search string: {search_string}\n")

for file in files:
    try:
        file_list = list(file)
    except UnicodeDecodeError:
        print(f"'{args.filename}' appears to be a binary file. Only text files are supported.")
        sys.exit(1)

    i = 0
    count = 0
    while i < len(file_list):
        line = file_list[i].rstrip()
        try:
            if args.ignore_case: matched = re.search(rf'{search_string}',line,re.I)
            else: matched = re.search(rf'{search_string}',line)
        except re.error as err:
            print(search_string)
            error_pos = re.search(r'([0-9]+)$',str(err)).group(0)
            print(" "*int(error_pos) + "^")
            print(f"Error compiling regular expression: {err}")
            sys.exit(1)

        if matched is not None and (args.max_count == 0 or count < args.max_count):
            matched_line = line
            if args.max_count > 0: count += 1
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
            if args.blank_line: print()
            continue
        i += 1
