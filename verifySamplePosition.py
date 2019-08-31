from random import *
from math import *
from time import *
from os import path
from pprint import *

currentTime=strftime("%b%d%Y_%Hh%Mm", localtime())
fieldBitSize=[32,32,16,16,8] # tuple5Size=[32,32,16,16,8]
# fieldBitSize=[32,64,48,48,16,12,3,20,3,32,32,8,6,16,16]
# fieldPosition=[0,32,96,144,192,208,220,223,243,246,278,310,318,324,340]
fieldPosition=[0,32,64,80,96]
# cbFileName=['acl_15','acl1_15','acl2_15','acl3_15']
cbFileName=['acl1_1k']


def loadClassBenchRuleFile(fileName, fieldSize):
    """
    Convert the decimal classbench rules into binary format and
    return a list of all the rules in [[field1, field2, field3, ... field5]] format

    """
    fop=open(fileName,'r')
    tempData=fop.readlines()
    fop.close()
    tuple5=[] #5 tuples with range extension
    for i in range(len(tempData)):
        #print(i)
        tuple5.append([])
        localTemp=tempData[i].replace('@','').split('\t')
        srcAddr=localTemp[0].split('/')[0].split('.')
        srcMask=localTemp[0].split('/')[1]
        dstAddr=localTemp[1].split('/')[0].split('.')
        dstMask=localTemp[1].split('/')[1]
        srcRang=localTemp[2].split(' : ')
        dstRang=localTemp[3].split(' : ')
        protocol=int(localTemp[4].split('/')[0],16)
        prtMask=int(localTemp[4].split('/')[1],16)
        #Source Address
        srcAddrString=''
        saLen=len(srcAddr)
        for j in range(saLen):
            temp=bin(int(srcAddr[j]))[2:]
            tLen=len(temp)
            if tLen<8:
                temp='0'*(8-tLen)+temp
            srcAddrString=srcAddrString+temp
        for j in range(int(srcMask),32):
            srcAddrString=srcAddrString[0:j]+'*'+srcAddrString[(j+1):]
        tuple5[i].append(srcAddrString)
        #Destination Address
        dstAddrString=''
        daLen=len(dstAddr)
        for j in range(daLen):
            temp=bin(int(dstAddr[j]))[2:]
            tLen=len(temp)
            if tLen<8:
                temp='0'*(8-tLen)+temp
            dstAddrString=dstAddrString+temp
        for j in range(int(dstMask),32):
            dstAddrString=dstAddrString[0:j]+'*'+dstAddrString[(j+1):]
        tuple5[i].append(dstAddrString)
        #Source Port
        if srcRang[0]==srcRang[1]:
            temp=bin(int(srcRang[1]))[2:]
            tLen=len(temp)
            srcRangStr='0'*(fieldSize[2]-tLen)+temp
            tuple5[i].append(srcRangStr)
        else:
            temp0=bin(int(srcRang[0]))[2:]
            temp1=bin(int(srcRang[1]))[2:]
            tLen0=len(temp0)
            tLen1=len(temp1)
            if tLen0==tLen1:
                xorValue=int(srcRang[0])^int(srcRang[1])
                tLen2=len(bin(xorValue)[2:])
                srcRangStr='0'*(fieldSize[2]-tLen1)+temp1[:(tLen1-tLen2)]+'*'*tLen2
            else:
                srcRangStr='0'*(fieldSize[2]-tLen1)+'*'*tLen1
            tuple5[i].append(srcRangStr)
        #Destination Port
        if dstRang[0]==dstRang[1]:
            temp=bin(int(dstRang[1]))[2:]
            tLen=len(temp)
            dstRangStr='0'*(fieldSize[3]-tLen)+temp
            tuple5[i].append(dstRangStr)
        else:
            temp0=bin(int(dstRang[0]))[2:]
            temp1=bin(int(dstRang[1]))[2:]
            tLen0=len(temp0)
            tLen1=len(temp1)
            if tLen0==tLen1:
                xorValue=int(dstRang[0])^int(dstRang[1])
                tLen2=len(bin(xorValue)[2:])
                dstRangStr='0'*(fieldSize[3]-tLen1)+temp1[:(tLen1-tLen2)]+'*'*tLen2
            else:
                dstRangStr='0'*(fieldSize[3]-tLen1)+'*'*tLen1
            tuple5[i].append(dstRangStr)
        # Protocol
        prtStr=bin(protocol)[2:]
        tLen=len(prtStr)
        if tLen<fieldSize[4]:
            prtStr='0'*(fieldSize[4]-tLen)+prtStr
        for j in range(prtMask,fieldSize[4]):
            prtStr=prtStr[0:j]+'*'+prtStr[(j+1):]
        tuple5[i].append(prtStr)

    return tuple5

def createRuleList(allfieldsRule):
    """
    """
    ruleList=[]

    for i in allfieldsRule:
        rule=''
        for k in i:
            # print(k, type(k))
            rule+=k
        ruleList.append(rule)

    return ruleList

# eBitPositions=[[34, 40, 87],[0, 2, 35, 89, 99],[1, 3, 32, 84, 99],[17, 33, 38, 87, 99]]
eBitPositions=[[30, 29, 39, 87, 101]]

for i in range(len(cbFileName)):
    ruleSubsetFromEffectiveBit={}
    fileLoc=cbFileName[i]
    # fileLoc='acl3_1K'
    cb5tupleTable=loadClassBenchRuleFile(fileLoc,fieldBitSize)
    # print(' 5 tuple rules= ', cb5tupleTable, '\nfirst rule = ', cb5tupleTable[0],len(cb5tupleTable),len(cb5tupleTable[0]),type(cb5tupleTable[0]))
    #print('A single 5 tuple rule= ', cb5tupleTable[0])
    rulesetNum=len(cb5tupleTable)
    #print('TotalNumber Of Rules= ', rulesetNum)
    allfieldsRule=createRuleList(cb5tupleTable)
    # print("allfieldsRule= ", allfieldsRule)
    # allfieldsTable=createAllfieldstable(allfieldsRule)  #original creates [['field1', 'field2', ...,'field15']]
                                                        # here [['field1field2..field5']] format is created
    allfieldsTable=cb5tupleTable[:]
    #print('5 field rule= ',allfieldsTable[0],len(allfieldsTable),len(allfieldsTable[0]),type(allfieldsTable[0]))
    # concatenatedRule=createConcatenatedRule(allfieldsRule)
    concatenatedRule=allfieldsRule[:]
    print(fileLoc, "All Rules= ")
    eBitPositionList=eBitPositions[i]
    ruleNumbersToverify=[]
    for ruleNumber in range (len(concatenatedRule)):
        # ruleMemberList=[]
        ruleNumbersToverify.append('R'+str(ruleNumber))
        rule=concatenatedRule[ruleNumber]
        eBitValue=''
        for position in eBitPositionList:
            eBitValue+=rule[position]
        rule+=' '+eBitValue
        if eBitValue in ruleSubsetFromEffectiveBit:
            ruleSubsetFromEffectiveBit[eBitValue].append('R'+str(ruleNumber))
        else:
            ruleSubsetFromEffectiveBit[eBitValue]=[]
            ruleSubsetFromEffectiveBit[eBitValue].append('R'+str(ruleNumber))
        print(rule)
    value=0
    for k in ruleSubsetFromEffectiveBit:
        print(k,':',ruleSubsetFromEffectiveBit[k],len(ruleSubsetFromEffectiveBit[k]))

    print("_______________________")
    ruleNumbersToverifyDuplicate=ruleNumbersToverify[:]
    # print(ruleSubsetFromEffectiveBit)

    #     for i in ruleNumbersToverify:
    #         if i in ruleSubsetFromEffectiveBit[k]:
    #             # print('Found', i)
    #             ruleNumbersToverify.remove(i)
    # print ('All the subsets from Effective bits ',ruleSubsetFromEffectiveBit)
    # print('Total rules before Checking= ', 'original= ', ruleNumbersToverify, 'duplicate= ', ruleNumbersToverifyDuplicate, len(ruleNumbersToverify),len(ruleNumbersToverifyDuplicate))
    #value=0
    for ruleNo in ruleNumbersToverify:
        for k in ruleSubsetFromEffectiveBit:
            if ruleNo in ruleSubsetFromEffectiveBit[k]:
                # value+=1
                ruleNumbersToverifyDuplicate.remove(ruleNo)

    print('Total rules after Checking= ', ruleNumbersToverifyDuplicate)
