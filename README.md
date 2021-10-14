# ARP Request Manipulator

## Intro

ARP Request Manipulator is a small network utility to allow users to manipulate and send customized ARP request packets by using [Scapy](https://scapy.net/). Following packet fields can be customized:

| Protocol Layer | Field Name |
| --- | --- |
| Ethernet | Source Address |
| Ethernet | Destination Address |
| ARP | Sender Hardware Address |
| ARP | Sender Protocol Address |
| ARP | Destination Hardware Address |
| ARP | Destination Protocol Address |

This utility ONLY sends ARP requests, it does not receive or process the responses. Please use tcpdump or WireShark to observe the response details.

## Python Module Dependencies

Following Python modules are needed to run this utility:

```
argparse
os
scapy
sys
```

## Usage

```
usage: arp-request-manipulator.py [-h] --ethersrc ETHERSRC [--etherdst ETHERDST] --arphwsrc ARPHWSRC [--arphwdst ARPHWDST] --arpipsrc ARPIPSRC --arpipdst ARPIPDST [--count COUNT]

ARP Request Packet Manipulator

optional arguments:
  -h, --help           show this help message and exit
  --ethersrc ETHERSRC  Ethernet source hardware address
  --etherdst ETHERDST  Ethernet destination hardware address (default: ff:ff:ff:ff:ff:ff)
  --arphwsrc ARPHWSRC  ARP sender hardware address
  --arphwdst ARPHWDST  ARP destination hardware address (default: 00:00:00:00:00:00)
  --arpipsrc ARPIPSRC  ARP source IP address
  --arpipdst ARPIPDST  ARP destination IP address
  --count COUNT        Number of APR requests will be sent (default: 1)
```

## Example

```
$ sudo ./arp-request-manipulator.py --ethersrc "aa:bb:cc:dd:ee:ff" --arphwsrc "aa:bb:cc:dd:ee:ff" --arpipsrc "192.168.0.81" --arpipdst "192.168.0.51" --count 5
##### Raw Packet Bytes #####
b'\xff\xff\xff\xff\xff\xff\xaa\xbb\xcc\xdd\xee\xff\x08\x06\x00\x01\x08\x00\x06\x04\x00\x01\xaa\xbb\xcc\xdd\xee\xff\xc0\xa8\x00Q\x00\x00\x00\x00\x00\x00\xc0\xa8\x003'

###[ Ethernet ]### 
  dst       = ff:ff:ff:ff:ff:ff
  src       = aa:bb:cc:dd:ee:ff
  type      = ARP
###[ ARP ]### 
     hwtype    = 0x1
     ptype     = IPv4
     hwlen     = 6
     plen      = 4
     op        = who-has
     hwsrc     = aa:bb:cc:dd:ee:ff
     psrc      = 192.168.0.81
     hwdst     = 00:00:00:00:00:00
     pdst      = 192.168.0.51

.....
Sent 5 packets.
```

## Technical Notes

1. In the book [TCP/IP Illustrated, Volume 1: The Protocols 2nd Edition](https://www.amazon.com/TCP-Illustrated-Protocols-Addison-Wesley-Professional/dp/0321336313) page 171:

```
For an ARP request, all the fields are filled in except the Target Hardware Address(which is set to 0).
```

This statement seems only a routine for the protocol. From the [ARP RFC 826](https://datatracker.ietf.org/doc/html/rfc826):

```
It does not set ar$tha to anything in particular, because it is this value that it is trying to determine. It could set ar$tha to the broadcast address for the hardware (all ones in the case of the 10Mbit Ethernet) if that makes it convenient for some aspect of the implementation.
```
