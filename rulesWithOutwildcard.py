from random import *
from math import *
from time import *
from os import path
from pprint import *
from ipaddress import *

fieldSize=[32,32,16,16,8]
cbFileName=['acl1_1k']
fileName=cbFileName[0]
fop=open(fileName,'r')
tempData=fop.readlines()
fop.close()
# print('tempData= ',tempData)
tuple5=[] #5 tuples with range extension

def ipMinMaxMean(network):
    """
    Take a network and output a mean IP/ IP thats in the middle of the
    Network
    """
    Network=network
    # print('Network=' ,Network)
    NetAddr=Network.split('/')[0].split('.')
    # print('NetAddr= ',NetAddr)
    NetMask=int(Network.split('/')[1])
    # print('NetMask= ',NetMask, type(NetMask))
    binAddr=''
    saLen=len(NetAddr)
    for j in range(saLen):
        temp=bin(int(NetAddr[j]))[2:]
        # print('NetAddr= ', NetAddr[j], temp)
        tLen=len(temp)
        if tLen<8:
            temp='0'*(8-tLen)+temp
        binAddr+=temp
    # print('binAddr',binAddr)
    networkBin=binAddr[:NetMask]
    hostBin=binAddr[NetMask:]
    # print(networkBin,len(networkBin))
    # print(hostBin,len(hostBin))
    # hostBinLen=len(hostBin)
    hostBinMin= '0'*len(hostBin)
    hostBinMax= '1'*len(hostBin)
    networkBinMin=networkBin+hostBinMin
    networkBinMax=networkBin+hostBinMax
    networkMin=int(networkBinMin,2)
    networkMax=int(networkBinMax,2)
    networkMeanInt=ceil((networkMin+networkMax)/2)
    return str(ip_address(networkMeanInt))
    # network4=ip_network(network)
    # # print('First IP= ', network4[0])
    # # print('last IP= ',network4[-1])
    # networkList=list(network4)
    # middleIPindex=ceil(len(networkList)/2)
    # print('middleIPindex= ', middleIPindex, 'NetworkLength= ', len(networkList))
    # if middleIPindex>=len(networkList):
    #     return str(networkList[0])
    # return str(networkList[middleIPindex])
    # # print('Length of the Network = ', len(networkList))

for i in range(len(tempData)):
    #print(i)
    tuple5.append([])
    localTemp=tempData[i].replace('@','').split('\t')
    srcNetwork=localTemp[0]
    print('localTemp= ', localTemp)
    print('srcNetwork=' ,srcNetwork)
    srcAddr=localTemp[0].split('/')[0].split('.')
    print('srcAddr= ',srcAddr)
    srcMask=localTemp[0].split('/')[1]
    print('srcMask= ',srcMask)
    dstNetwork=localTemp[1]
    print('dstNetwork= ', dstNetwork)
    dstAddr=localTemp[1].split('/')[0].split('.')
    print('dstAddr= ',dstAddr)
    dstMask=localTemp[1].split('/')[1]
    print('dstMask= ',dstMask)
    srcRang=localTemp[2].split(' : ')
    print('srcRang= ',srcRang)
    dstRang=localTemp[3].split(' : ')
    print('dstRang= ',dstRang)
    protocol=int(localTemp[4].split('/')[0],16)
    print('protocol= ',protocol)
    prtMask=int(localTemp[4].split('/')[1],16)
    print('prtMask= ',prtMask)

    #Source Address
    srcAddrString=''
    # meanAddr=0
    # numBerOfIP=0
    # for addr in IPv4Network(srcNetwork):
    #     meanAddr+=int(IPv4Address(addr))
    #     numBerOfIP+=1
    # meanAddr=ceil(meanAddr/numBerOfIP)
    # meanAddrIPv4=str(IPv4Address(meanAddr))
    meanAddrIPv4=ipMinMaxMean(srcNetwork)
    print(meanAddrIPv4)
    srcAddr=meanAddrIPv4.split('.')
    print('srcAddr=',srcAddr)
    saLen=len(srcAddr)
    for j in range(saLen):
        temp=bin(int(srcAddr[j]))[2:]
        print('srcAddr= ', srcAddr[j], temp)
        tLen=len(temp)
        if tLen<8:
            temp='0'*(8-tLen)+temp
        srcAddrString=srcAddrString+temp
    # print('srcAddr= ', srcAddrString)
    # for j in range(int(srcMask),32):
    #     srcAddrString=srcAddrString[0:j]+'*'+srcAddrString[(j+1):]
    print('srcAddrFinal= ', srcAddrString)
    tuple5[i].append(srcAddrString)
    #Destination Address
    dstAddrString=''
    # meanAddr=0
    # numBerOfIP=0
    # for addr in IPv4Network(dstNetwork):
    #     meanAddr+=int(IPv4Address(addr))
    #     numBerOfIP+=1
    # meanAddr=ceil(meanAddr/numBerOfIP)
    # meanAddrIPv4=str(IPv4Address(meanAddr))
    meanAddrIPv4=ipMinMaxMean(dstNetwork)
    dstAddr=meanAddrIPv4.split('.')
    print(meanAddrIPv4)
    daLen=len(dstAddr)
    for j in range(daLen):
        temp=bin(int(dstAddr[j]))[2:]
        print('dstAddr= ', dstAddr[j], temp)
        tLen=len(temp)
        if tLen<8:
            temp='0'*(8-tLen)+temp
        dstAddrString=dstAddrString+temp
    # for j in range(int(dstMask),32):
    #     dstAddrString=dstAddrString[0:j]+'*'+dstAddrString[(j+1):]
    print('dstAddrFinal= ', dstAddrString)
    tuple5[i].append(dstAddrString)

    #Source Port
    print('srcRange= ',int(srcRang[0]),int(srcRang[1]))
    if srcRang[0]==srcRang[1]:
        temp=bin(int(srcRang[1]))[2:]
        tLen=len(temp)
        srcRangStr='0'*(fieldSize[2]-tLen)+temp
        print('srcRangStr',srcRangStr)
        tuple5[i].append(srcRangStr)
    else:
        temp0=int(srcRang[0])
        temp1=int(srcRang[1])
        meanRng=ceil((temp0+temp1)/2)
        print('srcRangeMean=',meanRng)
        temp=bin(int(meanRng))[2:]
        tLen=len(temp)
        srcRangStr='0'*(fieldSize[2]-tLen)+temp
        print('srcRangStr',srcRangStr)
        tuple5[i].append(srcRangStr)
        # temp0=bin(int(srcRang[0]))[2:]
        # temp1=bin(int(srcRang[1]))[2:]
        # print('srcRange= ',int(srcRang[0]),int(srcRang[1]))
        # # print('srcRange= ',int(srcRang[0]),int(srcRang[1]))
        # print('temp0',temp0)
        # print('temp1',temp1)
        # tLen0=len(temp0)
        # tLen1=len(temp1)
        # if tLen0==tLen1:
        #     xorValue=int(srcRang[0])^int(srcRang[1])
        #     tLen2=len(bin(xorValue)[2:])
        #     srcRangStr='0'*(fieldSize[2]-tLen1)+temp1[:(tLen1-tLen2)]+'*'*tLen2
        # else:
        #     srcRangStr='0'*(fieldSize[2]-tLen1)+'*'*tLen1
        # tuple5[i].append(srcRangStr)

    #Destination Port

    print('dstRange= ',int(dstRang[0]),int(dstRang[1]))
    if dstRang[0]==dstRang[1]:
        temp=bin(int(dstRang[1]))[2:]
        tLen=len(temp)
        dstRangStr='0'*(fieldSize[3]-tLen)+temp
        print('dstRangStr',dstRangStr)
        tuple5[i].append(dstRangStr)
    else:
        temp0=int(dstRang[0])
        temp1=int(dstRang[1])
        meanRng=ceil((temp0+temp1)/2)
        print('dstRangeMean=',meanRng)
        temp=bin(int(meanRng))[2:]
        tLen=len(temp)
        dstRangStr='0'*(fieldSize[3]-tLen)+temp
        print('dstRangStr',dstRangStr)
        tuple5[i].append(dstRangStr)
        # temp0=bin(int(dstRang[0]))[2:]
        # temp1=bin(int(dstRang[1]))[2:]
        # tLen0=len(temp0)
        # tLen1=len(temp1)
        # if tLen0==tLen1:
        #     xorValue=int(dstRang[0])^int(dstRang[1])
        #     tLen2=len(bin(xorValue)[2:])
        #     dstRangStr='0'*(fieldSize[3]-tLen1)+temp1[:(tLen1-tLen2)]+'*'*tLen2
        # else:
        #     dstRangStr='0'*(fieldSize[3]-tLen1)+'*'*tLen1
        # tuple5[i].append(dstRangStr)
    # Protocol
    print('protocol', protocol,'prtMask', prtMask)
    if protocol >0 and prtMask >0:
        prtStr=bin(protocol)[2:]
        tLen=len(prtStr)
        if tLen<fieldSize[4]:
            prtStr='0'*(fieldSize[4]-tLen)+prtStr
        # for j in range(prtMask,fieldSize[4]):
        #     prtStr=prtStr[0:j]+'*'+prtStr[(j+1):]
        print('prtStr', prtStr)
        tuple5[i].append(prtStr)
    else:
        meanprotocol=128 #ceil(prtMask/2)
        prtStr=bin(meanprotocol)[2:]
        tLen=len(prtStr)
        print('prtStrBinary', prtStr,'length', tLen)
        if tLen<fieldSize[4]:
            prtStr='0'*(fieldSize[4]-tLen)+prtStr
        print('prtStr', prtStr)
        tuple5[i].append(prtStr)

print('tuple5', tuple5)
