"""
Read a Cisco configuration file and interpret it the same as:
  show command output | section <pattern-to-match>

This uses Python's "re" module adapted to Cisco's regex parser... it is not a
perfect match. Be particularly careful when using the _ character, though it
generally works fine.

See https://www.cisco.com/en/US/products/sw/iosswrel/ps1835/products_configuration_guide_chapter09186a00803479f1.html
"""

import sys, os, re

# if insufficient parameters are specified
if len(sys.argv) < 2:
    program = sys.argv[0]
    if hasattr(sys, '_MEIPASS'):
        program = sys.executable
    print("Read a Cisco configuration file and interpret it the same as:")
    print("  show command output | section <pattern-to-match>\n")
    print(f'Syntax: {program} "pattern to match" [filename]\n')
    print("  quotes are required if pattern has spaces\n")
    print(f'Example: {program} "^interface Vlan10_" core9500.cfg\n')
    print("If filename is not specified, it will read from STDIN")
    sys.exit(1)

def ctrlc(type,*args):
    "Ctrl+C handler"
    if type==KeyboardInterrupt:
        print("!!! Terminated by ^C !!!")
        sys.exit()
    else:
        sys.__excepthook__(type,*args)

sys.excepthook = ctrlc

if (len(sys.argv) > 2):
    # if a wildcard was used to specify a file
    if "*" in sys.argv[2] or "?" in sys.argv[2]:
        from glob import glob
        filepath = glob(sys.argv[2])[0]
        print(f"Processing {filepath}\n-----")
    else:
        filepath = sys.argv[2]

if not 'filepath' in locals():
    # File not specified; read from stdin
    file = sys.stdin
elif not os.path.isfile(filepath):
    # File specified but not found
    print(f"File {filepath} not found")
    sys.exit(1)
else:
    # File specified and found
    file = open(filepath)

try:
    file_list = list(file)
except UnicodeDecodeError:
    print(f"'{filepath}' appears to be a binary file. Only text files are supported.")
    sys.exit(1)

search_string = sys.argv[1].replace("_","([_\)\({},\s]|^|$)")

verbose = True
if verbose:
    print(f"Interpreted search string: {search_string}\n")

i = 0
while i < len(file_list):
    line = file_list[i].rstrip()
    #search_string = sys.argv[2].replace("_","([_}{,\)\()(\s]|^|$)")
    try:
        matched = re.search(rf'{search_string}',line)
    except re.error as err:
        print(search_string)
        error_pos = re.search(r'([0-9]+)$',str(err)).group(0)
        print(" "*int(error_pos) + "^")
        print(f"Error compiling regular expression: {err}")
        sys.exit(1)

    if matched is not None:
        matched_line = line
        print(matched_line)
        while True:
            i += 1
            try:
                current_line = file_list[i].rstrip()
            except IndexError:
                # end-of-file was reached
                sys.exit(0)
            current_line_whitespace_index = re.search(r'\S',current_line)
            matched_line_whitespace_index = re.search(r'\S',matched_line)
            if current_line_whitespace_index is not None and matched_line_whitespace_index is not None:
                if re.search(r'\S',current_line).start() > re.search(r'\S',matched_line).start():
                    print(current_line)
                else:
                    break
        continue
    i += 1
