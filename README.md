# section

Mimics the behavior of Cisco IOS's ```| section ...``` command. Just like IOS, it supports parsing through a file and viewing sections of matched data. Like IOS, it supports _ as a blank, end-of-line, etc., ([see here](https://www.cisco.com/en/US/products/sw/iosswrel/ps1835/products_configuration_guide_chapter09186a00803479f1.html)) for things like interfaces (for example, Gi1/1/1_ would not show Gi1/1/10, Gi1/1/11, etc). Requires Python 3.6 or higher.

Cisco IOS Example: ```show run brief | sec ^crypto (ipsec|isakmp)```

Read a file and interpret it the same as:
  show command output | section <pattern-to-match>

Examples:
* ```python3 section.py "^interface Vlan10_" core9500.cfg```
* ```cat core9500.cfg | python3 section.py "^interface Vlan10_"```

Usage: section [options] "pattern to match" [filename]

positional arguments:
  pattern-to-match      pattern to match; quotes are required if pattern contains spaces; supports regex
  filename              file to read from; if not specified, read from STDIN

optional arguments:
  -h, --help            show this help message and exit
  -i, --ignore-case     ignore case distinctions
  -m NUM, --max-count NUM
                        stop after NUM matches
  -n, --line-number     print line number with output lines
  -b, --add-blank       add a blank line between matched sections for readability
  -v, --verbose         show pattern that will be matched
