from math import *
from ipaddress import *

def ipMinMaxMean(network):
    """
    Take a network and output a mean IP/ IP thats in the middle of the
    Network
    """
    Network=network
    print('Network=' ,Network)
    NetAddr=Network.split('/')[0].split('.')
    print('NetAddr= ',NetAddr)
    NetMask=int(Network.split('/')[1])
    print('NetMask= ',NetMask, type(NetMask))
    binAddr=''
    saLen=len(NetAddr)
    for j in range(saLen):
        temp=bin(int(NetAddr[j]))[2:]
        print('NetAddr= ', NetAddr[j], temp)
        tLen=len(temp)
        if tLen<8:
            temp='0'*(8-tLen)+temp
        binAddr+=temp
    print('binAddr',binAddr)
    networkBin=binAddr[:NetMask]
    hostBin=binAddr[NetMask:]
    print(networkBin,len(networkBin))
    print(hostBin,len(hostBin))
    hostBinLen=len(hostBin)
    hostBinMin= '0'*len(hostBin)
    hostBinMax= '1'*len(hostBin)
    networkBinMin=networkBin+hostBinMin
    networkBinMax=networkBin+hostBinMax
    networkMin=int(networkBinMin,2)
    networkMax=int(networkBinMax,2)
    networkMeanInt=ceil((networkMin+networkMax)/2)
    return str(ip_address(networkMeanInt))


    # else:
network='0.0.0.0/0'
print(ipMinMaxMean(network))
# net4 = ip_network(network)
# for x in net4.hosts():
#     # print(x)



    # network4=ip_network(network)
    # print('First IP= ', network4[0])
    # print('last IP= ',network4[-1])
    # networkList=list(network4)
    # middleIPindex=ceil(len(networkList)/2)
    # print('middleIPindex= ', middleIPindex, 'NetworkLength= ', len(networkList))
    # if middleIPindex>=len(networkList):
        # return str(networkList[0])
    # return str(networkList[middleIPindex])
    # print('Length of the Network = ', len(networkList))
