# section
Mimics the behavior of Cisco IOS's "| section ..." command

Requires Python 3.6 or higher

Read a Cisco configuration file and interpret it the same as:
  show command output | section <pattern-to-match>

Syntax: python3 section.py "\<pattern-to-match\>" \<filename\>

  quotes are required if pattern has spaces

Example: python3 section.py "^interface Vlan10_" core9500.cfg

Just like Cisco IOS, it supports parsing through a file and viewing sections of matched data. Like IOS, it supports _ as a blank, end-of-line, etc., ([see here](https://www.cisco.com/en/US/products/sw/iosswrel/ps1835/products_configuration_guide_chapter09186a00803479f1.html)) for things like interfaces (for example, Gi1/1/1_ would not show Gi1/1/10, Gi1/1/11, etc).
