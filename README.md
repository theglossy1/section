# section
Mimics the behavior of Cisco IOS's "| section ..." command

Requires Python 3.6 or higher

Syntax: section.py <filename> <regex>
  
Just like Cisco IOS. It supports parsing through a file and viewing sections of matched data. Like IOS, it supports _ as a blank character or end-of-line, for things like interfaces (for example, Gi1/1/1_ would not show Gi1/1/10, Gi1/1/11, etc).

The regex supports anything supported by Python's re module, which is the same POSIX extended Regex that IOS uses (with a few extras thrown in).
