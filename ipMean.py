# import ipaddress
from ipaddress import *
# import math
from math import *
network='192.0.0.0/8'
meanAddr=0
numBerOfIP=0
for addr in IPv4Network(network):
    meanAddr+=int(IPv4Address(addr))
    numBerOfIP+=1
meanAddr=ceil(meanAddr/numBerOfIP)
meanAddrIPv4=IPv4Address(meanAddr)
print(meanAddrIPv4)
