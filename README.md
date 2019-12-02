# section
Mimics the behavior of Cisco IOS's "| section ..." command

Requires Python 3.6 or higher

Read a Cisco configuration file and interpret it the same as:
  show command output | section <pattern-to-match>

Syntax: c:\batch\section.py <filename> "<pattern-to-match>"

  quotes are required if pattern has spaces

Example: c:\batch\section.py core9500.cfg "^interface Vlan10_"

Just like Cisco IOS, it supports parsing through a file and viewing sections of matched data. Like IOS, it supports _ as a blank, end-of-line, etc. ([see here](https://www.cisco.com/en/US/products/sw/iosswrel/ps1835/products_configuration_guide_chapter09186a00803479f1.html)) for things like interfaces (for example, Gi1/1/1_ would not show Gi1/1/10, Gi1/1/11, etc).

The regex supports anything supported by Python's re module, which is the same POSIX extended Regex that IOS uses (with a few extras thrown in).
