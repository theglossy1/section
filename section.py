import sys, os, re

if len(sys.argv) < 3:
    program = sys.argv[0]
    if hasattr(sys, '_MEIPASS'):
        program = sys.executable
    print(f'Syntax: {program} <filename> <regex>')
    sys.exit()

filepath = sys.argv[1]
if not os.path.isfile(filepath):
    print(f"File path '{filepath}' does not exist.")
    sys.exit(1)

file = open(sys.argv[1])
try:
    file_list = list(file)
except UnicodeDecodeError:
    print(f"'{filepath}' appears to be a binary file. Only text files are supported.")
    quit(1)

i = 0
while i < len(file_list):
    line = file_list[i].rstrip()
    search_string = sys.argv[2].replace("_","(\s|$)")
    matched = re.search(rf'{search_string}',line)
    if matched is not None:
        matched_line = line
        print(matched_line)
        while True:
            i += 1
            current_line = file_list[i].rstrip()
            current_line_whitespace_index = re.search(r'\S',current_line)
            matched_line_whitespace_index = re.search(r'\S',matched_line)
            if current_line_whitespace_index is not None and matched_line_whitespace_index is not None:
                if re.search(r'\S',current_line).start() > re.search(r'\S',matched_line).start():
                    print(current_line)
                else:
                    break
        continue
    i += 1