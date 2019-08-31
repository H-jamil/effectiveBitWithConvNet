from ipaddress import *
# import math
from math import *
network='192.0.0.0/8'
meanAddr=0

network4=ip_network(network)
print('First IP= ', network4[0])
print('last IP= ',network4[-1])
networkList=list(network4)
print('Length of the Network = ', len(networkList))
middleIPindex=ceil(len(networkList)/2)
print('middleIPindex= ', middleIPindex, 'NetworkLength= ', len(networkList))
if middleIPindex>=len(networkList):
    print(str(networkList[0]))
print(str(networkList[middleIPindex]))
