from random import *
from math import *
from time import *
import os
from pprint import *
from ipaddress import *

currentTime=strftime("%b%d%Y_%Hh%Mm", localtime())
fieldBitSize=[32,32,16,16,8] # tuple5Size=[32,32,16,16,8]
# fieldBitSize=[32,64,48,48,16,12,3,20,3,32,32,8,6,16,16]
# fieldPosition=[0,32,96,144,192,208,220,223,243,246,278,310,318,324,340]
fieldPosition=[0,32,64,80,96]

# qRatio=[0.02,0.02,0.25,0.25,0.01,0.2,1,0.02,1,0.25,0.25,0.02,1,0.1,0.1]
bitspaceSize=1
fieldNum=len(fieldBitSize)
wRatio=0.1
#cFactor=[0.9,0.9,0.9,0.9,0.9,0.8,0.8,0.8,0.8,0.9,0.9,0.9,0.5,0.8,0.8]
cFactor=[0.9,0.9,0.8,0.8,0.9]
# cbFileName=['acl_15','acl1_15','acl2_15','acl3_15']
# cwd=os.getcwd()
# cbFileName=os.listdir(cwd)
# cbFileName=cbFileName[:-1]
# cbFileName=['acl1_1k_0', 'acl1_1k_1', 'acl1_1k_2', 'acl1_1k_3', 'acl1_1k_4', 'acl1_1k_5','acl1_1k_wildcards']
# cbFileName=['acl1_1k']
cbFileName=['acl1_500']

# cbFileName=['acl1_1k']
# dcRatioMulti=[[0.10,0.10,0.10,0.10,0.10,0.50,0.50,0.50,0.50,1,1,1,0.50,1,1]]
samplePos=[]

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

def checkBitChr(allfieldsTable,fieldBitSize):
    #allfieldsTable[rule][field][bit]
    bChr=[]
    for i in range(len(allfieldsTable[0])):
        bChr.append([[],[]]) #[0] for WC, [1] for 0/1 ratio

    fNum=len(allfieldsTable[0]) # of field
    rNum=len(allfieldsTable) # of rule
    for field in range(fNum):
        for bit in range(fieldBitSize[field]):
            countW=0
            count0=0
            count1=0
            for rule in range(rNum):
                if allfieldsTable[rule][field][bit]=='*':
                    countW+=1
                elif allfieldsTable[rule][field][bit]=='0':
                    count0+=1
                elif allfieldsTable[rule][field][bit]=='1':
                    count1+=1
            bChr[field][0].append(countW/rNum)
            bChr[field][1].append(count0/rNum*count1/rNum)
    return bChr

def getFieldWC(bitCharTable):
    fWC=[]
    index=1
    for i in range(len(bitCharTable)):
        minFieldWC=min(bitCharTable[i][0])
        if fWC.count(minFieldWC)>0:
            fWC.append((minFieldWC+index/10000)) # make fields with same DC ratio looks different
            index+=1
        else:
            fWC.append(minFieldWC)
    return fWC

def pickPos4SMatrix(bitCharTable):
    p4sm=[]
    fNum=len(bitCharTable)
    for i in range(fNum):
        p4sm.append(bitCharTable[i][1].index(max(bitCharTable[i][1])))
    return p4sm

def getSimilariyCheckForTwoBitPos(rule,field,BitPos1,BitPos2):
    condt1=(allfieldsTable[rule][field][BitPos1] != allfieldsTable[rule][field][BitPos2])
    condt2=(allfieldsTable[rule][field][BitPos1] != '*')
    condt3=(allfieldsTable[rule][field][BitPos2] != '*')
    return (condt1 and condt2 and condt3)

def getSimilarityMatrix(pos4SMatrix,allfieldsTable,fieldBitSize):
    sMatrix=[]
    fNum=len(allfieldsTable[0]) # of field
    rNum=len(allfieldsTable) # of rule
    for field in range(fNum):
        sMatrix.append([])
        for bit in range(fieldBitSize[field]):
            countDiff=0
            for rule in range(rNum):
                if getSimilariyCheckForTwoBitPos(rule,field,pos4SMatrix[field],bit):
                    countDiff+=1
            sMatrix[field].append(countDiff)

        for bit in range(len(sMatrix[field])):
            subBit=[i for i,x in enumerate(sMatrix[field]) if x == sMatrix[field][bit]]
            tempLen=len(subBit)
            if tempLen>1:
                index=1
                for subBitPos in range(tempLen-1):
                    subCountDiff=0
                    for rule in range(rNum):
                        if getSimilariyCheckForTwoBitPos(rule,field,subBit[0],subBit[subBitPos+1]):
                            subCountDiff+=1
                    if subCountDiff<10: # if two bitPos are the same, use non-zero small value for the following field
                        sMatrix[field][subBit[subBitPos+1]]=index
                        index+=1
                    else: # if two bitPos are not the same, take one index value out for the following field
                        sMatrix[field][subBit[subBitPos+1]]-=index
    return sMatrix

def getBitPosCandidateList(fieldWC,fieldBitSize,bitCharTable,similarityMatrix,cFactor):
    BPCList=[]
    fNum=len(fieldWC)
    uBPCList=[]

    for i in range(fNum): # i is fieldPos
        BPCList.append([])
        uBPCList.append([])
        fSMatrix=similarityMatrix[i]
        sortedFSMatrix=sorted(fSMatrix,reverse=True)
##        print(i)
        maxFieldValue=max(bitCharTable[i][1]) #Get the max DiffCount
        #Include the one with lowest WC in a field
        #check itself generate 0, but this bit pos is with lowest WC!
        bitPos=fSMatrix.index(0)

        for j in range(fSMatrix.count(0)):
            sortedFSMatrix.pop(-1)
##        print(bitPos)
##        print(bitCharTable[i][1][bitPos])
##        print(maxFieldValue)
        if maxFieldValue>0:
            if (bitCharTable[i][1][bitPos]/maxFieldValue)>cFactor[i]:
                BPCList[i].append(bitPos)
        #Check the rest
        while len(sortedFSMatrix)>0:
            bitPos=fSMatrix.index(sortedFSMatrix.pop(0))#Get bit position from highest DiffCount
            if maxFieldValue>0:
                testValue=bitCharTable[i][1][bitPos]/maxFieldValue
                if testValue>cFactor[i]:
                    BPCList[i].append(bitPos)
                else:
                    uBPCList[i].append(bitPos)
    return BPCList

def createFWCDiff(fieldWC):
    fieldWCDiff=[]
    avgFieldWC=sum(fieldWC)/len(fieldWC)
    for i in range(len(fieldWC)):
        tIndex=1
        tmpDiff=fieldWC[i]-avgFieldWC
        if fieldWCDiff.count(tmpDiff)>0:
            fieldWCDiff.append(tmpDiff-tmpIndex/10000)
            tmpIndex+=1
        else:
            fieldWCDiff.append(tmpDiff)
    return fieldWCDiff

def createFieldReplaceList(fieldWCDiff,bitPosCandidateList,bitspaceSize):
    rFieldList=[] #rFieldList[bitspace][replace set]
    candidateCount=createCandidateCount(bitPosCandidateList)

    for i in range(bitspaceSize):
        #print(candidateCount)
        rFieldList.append([])
        sortedFieldWCDiff=sorted(fieldWCDiff,reverse=True)
        if len(sortedFieldWCDiff)>1:
            poorWC=sortedFieldWCDiff.pop(0)
            goodWC=sortedFieldWCDiff.pop(-1)
            while(poorWC>0.15 and goodWC <0):
                goodField=fieldWCDiff.index(goodWC)
                if candidateCount[goodField]>=2:#Good field need to have at least 2 bits
                    poorField=fieldWCDiff.index(poorWC)
                    rFieldList[i].append([goodField,poorField])
                    candidateCount[goodField]-=2 # Each position needs 2 samples when it is chose
                    #print(goodField,poorField)
                    if len(sortedFieldWCDiff)>1:
                        poorWC=sortedFieldWCDiff.pop(0)
                        goodWC=sortedFieldWCDiff.pop(-1)
                    else:
                        goodWC=1
                else:
                    if len(sortedFieldWCDiff)>0:
                        goodWC=sortedFieldWCDiff.pop(-1)
                    else:
                        goodWC=1
    #print(candidateCount)
    #print(rFieldList)
    return rFieldList

def createCandidateCount(bitPosCandidateList):
    candCount=[]
    for i in range(len(bitPosCandidateList)):
        candCount.append(len(bitPosCandidateList[i]))
    return candCount

def createSamplePos(bitPosCandidateList,fieldReplaceList,bitspaceSize,fieldPosition):
    sPos=[]
    fNum=len(bitPosCandidateList)

    for b in range(bitspaceSize):
        candidateCount=createCandidateCount(bitPosCandidateList)
        print(candidateCount)
        fieldList=[]
        #print(b,fieldReplaceList[b])
        sPos.append([])
        for i in range(fNum):
            if candidateCount[i]>0:
                fieldList.append(1) # Each space give 1 as default
            else:
                fieldList.append(0)
        rpNum=len(fieldReplaceList[b])
        for i in range(rpNum):
            if candidateCount[fieldReplaceList[b][i][0]]>1:
                fieldList[fieldReplaceList[b][i][0]]+=1 # Need additional sample on this field
                if candidateCount[fieldReplaceList[b][i][1]]>0:
                    fieldList[fieldReplaceList[b][i][1]]-=1 # Remove the sample
        print(fieldList)
        #print(bitPosCandidateList)
        for i in range(fNum):
            sNum=fieldList[i]
            for j in range(sNum):
                print(i,j)
                sPos[b].append(fieldPosition[i]+bitPosCandidateList[i].pop(0))
    #print(sPos)
    return sPos

def createCandidateCount(bitPosCandidateList):
    candCount=[]
    for i in range(len(bitPosCandidateList)):
        candCount.append(len(bitPosCandidateList[i]))
    return candCount

def createIndexList(fieldBitSize,fieldReplaceList,bitspaceSize,fieldWC,indexSize,bitPosCandidateList):
    iList=[]

    fNum=len(fieldBitSize)

    candidateCount=createCandidateCount(bitPosCandidateList)
    #print(candidateCount)
    for b in range(bitspaceSize):
        rpNum=len(fieldReplaceList[b])
        iList.append([])
        sFWC=sorted(fieldWC)
        uFWC=list(fieldWC)
        for i in range(fNum):
            if candidateCount[i]>0:
                iList[b].append(1)
                candidateCount[i]-=1
            else:
                iList[b].append(0)
                #sFWC.pop(sFWC.index(fieldWC[i]))
                uFWC.pop(uFWC.index(fieldWC[i]))
                #print(i,len(uFWC))

        for i in range(rpNum):
            #print(b,i,fieldReplaceList[b])
            field0=fieldReplaceList[b][i][0]
            field1=fieldReplaceList[b][i][1]
            #print(candidateCount)
            if candidateCount[field0]>0: #Replace only when we have more bits available in low WC field
                candidateCount[field0]-=1
                iList[b][field0]+=1
                if uFWC.count(fieldWC[field1])>0:
                    #print(field0,field1,uFWC.count(fieldWC[field0]),uFWC.count(fieldWC[field1]))
                    uFWC[uFWC.index(fieldWC[field1])]=uFWC[uFWC.index(fieldWC[field0])]
                else:
                    uFWC.append(fieldWC[field0])
            elif uFWC.count(fieldWC[field1])>0:
                uFWC.pop(uFWC.index(fieldWC[field1]))
            iList[b][field1]=0

        sFWC2=sorted(uFWC)
        #zeroNum=iList[b].count(0)
        oneNum=iList[b].count(1)
        twoNum=iList[b].count(2)
        avlBitNum=oneNum+twoNum*2
        topFieldList=[]
        for i in range(len(iList[b])):
            if iList[b][i]==2:
                topFieldList.append(fieldWC[i])
        sTopFieldList=sorted(topFieldList)

        diffNum=avlBitNum-indexSize

        if diffNum<0:
            for i in range(abs(diffNum)):
                if len(fieldReplaceList[b])>0:
                # Take the replaced bit back to fulfill indexSize requirement
                    tempFR=fieldReplaceList[b].pop()[1]
                else:
                # Use the lowest WC field who still have available bit positions
                    findBestSubField=False
                    addr=0
                    while findBestSubField==False:
                        tempFR=fieldWC.index(sFWC[addr])
                        if candidateCount[tempFR]>0:
                            findBestSubField=True
                        addr+=1

                iList[b][tempFR]+=1

        else:
            for i in range(diffNum):
                if i<twoNum: # reduce bits from fields with 2 samples first
                    value=sTopFieldList.pop()
                    sFWC2.pop(sFWC2.index(value))
                    pos=fieldWC.index(value)
                    iList[b][pos]-=1
                else:
                    value=sFWC2.pop()
                    pos=fieldWC.index(value)
                    iList[b][pos]-=1
        #print(b,iList[b])
    #print(iList)
    return iList

def getIndexPos(indexList,fieldPosition, bitPosCandidateList):
    iPos=[]
    for i in range(len(indexList)): #get bitspaceSize
        iPos.append([])
        #if indexList[i]==1:
        for j in range(len(indexList[i])):# get fieldNum
            for k in range(indexList[i][j]):
                #print(i,j)
                iPos[i].append(fieldPosition[j]+bitPosCandidateList[j].pop(0))
    return iPos

def createIndexBitmap(indexPos,concatenatedRule):
    #allfieldsTable[rule][field][bit]
    rIndexBitmap=[]
    rNum=len(concatenatedRule)
    for b in range(len(indexPos)):
        rIndexBitmap.append([])
        for i in range(rNum):
            temp=''
            iSize=len(indexPos[b])
            if iSize==0:
                temp='0'
            else:
                for j in range(iSize):
                    temp=temp+concatenatedRule[i][indexPos[b][j]]
            rIndexBitmap[b].append(temp)
    return rIndexBitmap

def createExtTable(bitmap):
    extBitmap=[]
    bNum=len(bitmap)
    for b in range(bNum):
        extBitmap.append([])
        rNum=len(bitmap[b])
        for i in range(rNum):
            extBitmap[b].append([])
            eTable=[]
            countWC=bitmap[b][i].count('*')
            extNum=int(pow(2,countWC))

            for k in range(extNum):
                temp=bin(k)[2:]
                tlen=len(temp)
                if tlen<countWC:
                    temp='0'*(countWC-tlen)+temp
                eTable.append(temp)

            for k in range(extNum):
                tmp=str(bitmap[b][i])
                for x in range(countWC):
                    tPos=tmp.find('*')
                    tmp=tmp[:tPos]+eTable[k][x]+tmp[(tPos+1):]
                #print(tmp)
                extBitmap[b][i].append(int(tmp,2)) #extBitmap[bitspace][rule]
    return extBitmap

def createIndexLookup(indexSize,extendedIndexBitmapTable):
    iLookup=[]
    for b in range(len(extendedIndexBitmapTable)):
        iLookup.append([])
        for i in range(int(pow(2,indexSize))):
            iLookup[b].append([])
    for b in range(len(extendedIndexBitmapTable)):
        for i in range(len(extendedIndexBitmapTable[b])):
            for j in range(len(extendedIndexBitmapTable[b][i])):
                iLookup[b][extendedIndexBitmapTable[b][i][j]].append(i)
    return iLookup

def createRuleList(allfieldsRule):
    """
    """
    ruleList=[]

    for i in allfieldsRule:
        rule=''
        for k in i:
            rule+=k
        ruleList.append(rule)

    return ruleList
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


def rulesWithoutWildCardBits(fileName,fieldSize):
    tupleWithoutWildCard5=[]
    fop=open(fileName,'r')
    tempData1=fop.readlines()
    fop.close()
    for i in range(len(tempData1)):
        #print(i)
        tupleWithoutWildCard5.append([])
        localTemp=tempData1[i].replace('@','').split('\t')
        srcNetwork=localTemp[0]
        # print('localTemp= ', localTemp)
        # print('srcNetwork=' ,srcNetwork)
        srcAddr=localTemp[0].split('/')[0].split('.')
        # print('srcAddr= ',srcAddr)
        srcMask=localTemp[0].split('/')[1]
        # print('srcMask= ',srcMask)
        dstNetwork=localTemp[1]
        # print('dstNetwork= ', dstNetwork)
        dstAddr=localTemp[1].split('/')[0].split('.')
        # print('dstAddr= ',dstAddr)
        dstMask=localTemp[1].split('/')[1]
        # print('dstMask= ',dstMask)
        srcRang=localTemp[2].split(' : ')
        # print('srcRang= ',srcRang)
        dstRang=localTemp[3].split(' : ')
        # print('dstRang= ',dstRang)
        protocol=int(localTemp[4].split('/')[0],16)
        # print('protocol= ',protocol)
        prtMask=int(localTemp[4].split('/')[1],16)
        # print('prtMask= ',prtMask)

        #Source Address
        srcAddrString=''

        meanAddrIPv4=ipMinMaxMean(srcNetwork)
        # print(meanAddrIPv4)
        srcAddr=meanAddrIPv4.split('.')
        # print('srcAddr=',srcAddr)
        saLen=len(srcAddr)
        for j in range(saLen):
            temp=bin(int(srcAddr[j]))[2:]
            # print('srcAddr= ', srcAddr[j], temp)
            tLen=len(temp)
            if tLen<8:
                temp='0'*(8-tLen)+temp
            srcAddrString=srcAddrString+temp

        tupleWithoutWildCard5[i].append(srcAddrString)
        #Destination Address
        dstAddrString=''

        meanAddrIPv4=ipMinMaxMean(dstNetwork)
        dstAddr=meanAddrIPv4.split('.')
        # print(meanAddrIPv4)
        daLen=len(dstAddr)
        for j in range(daLen):
            temp=bin(int(dstAddr[j]))[2:]
            # print('dstAddr= ', dstAddr[j], temp)
            tLen=len(temp)
            if tLen<8:
                temp='0'*(8-tLen)+temp
            dstAddrString=dstAddrString+temp

        tupleWithoutWildCard5[i].append(dstAddrString)

        #Source Port
        # print('srcRange= ',int(srcRang[0]),int(srcRang[1]))
        if srcRang[0]==srcRang[1]:
            temp=bin(int(srcRang[1]))[2:]
            tLen=len(temp)
            srcRangStr='0'*(fieldSize[2]-tLen)+temp
            # print('srcRangStr',srcRangStr)
            tupleWithoutWildCard5[i].append(srcRangStr)
        else:
            temp0=int(srcRang[0])
            temp1=int(srcRang[1])
            meanRng=ceil((temp0+temp1)/2)
            # print('srcRangeMean=',meanRng)
            temp=bin(int(meanRng))[2:]
            tLen=len(temp)
            srcRangStr='0'*(fieldSize[2]-tLen)+temp
            # print('srcRangStr',srcRangStr)
            tupleWithoutWildCard5[i].append(srcRangStr)


        #Destination Port

        # print('dstRange= ',int(dstRang[0]),int(dstRang[1]))
        if dstRang[0]==dstRang[1]:
            temp=bin(int(dstRang[1]))[2:]
            tLen=len(temp)
            dstRangStr='0'*(fieldSize[3]-tLen)+temp
            # print('dstRangStr',dstRangStr)
            tupleWithoutWildCard5[i].append(dstRangStr)
        else:
            temp0=int(dstRang[0])
            temp1=int(dstRang[1])
            meanRng=ceil((temp0+temp1)/2)
            # print('dstRangeMean=',meanRng)
            temp=bin(int(meanRng))[2:]
            tLen=len(temp)
            dstRangStr='0'*(fieldSize[3]-tLen)+temp
            # print('dstRangStr',dstRangStr)
            tupleWithoutWildCard5[i].append(dstRangStr)

        if protocol >0 and prtMask >0:
            prtStr=bin(protocol)[2:]
            tLen=len(prtStr)
            if tLen<fieldSize[4]:
                prtStr='0'*(fieldSize[4]-tLen)+prtStr
            # print('prtStr', prtStr)
            tupleWithoutWildCard5[i].append(prtStr)
        else:
            meanprotocol=128 #ceil(prtMask/2)
            prtStr=bin(meanprotocol)[2:]
            tLen=len(prtStr)
            # print('prtStrBinary', prtStr,'length', tLen)
            if tLen<fieldSize[4]:
                prtStr='0'*(fieldSize[4]-tLen)+prtStr
            # print('prtStr', prtStr)
            tupleWithoutWildCard5[i].append(prtStr)

    return  tupleWithoutWildCard5
    #     ruleList=[]
    #     for i in tupleWithoutWildCard5:
    #         rule=''
    #         for k in i:
    #             # print(k, type(k))
    #             rule+=k
    #         ruleList.append(rule)
    #
    # return ruleList

def verificationOfRuleset(cb5tupleTable,samplePos,printcommand):
    ruleSubsetFromEffectiveBit={}
    allfieldsRule=createRuleList(cb5tupleTable)
    allfieldsTable=cb5tupleTable[:]
    concatenatedRule=allfieldsRule[:]
    eBitPositionList=samplePos[:]
    ruleNumbersToverify=[]
    for ruleNumber in range (len(concatenatedRule)):
        ruleNumbersToverify.append('R'+str(ruleNumber))
        rule=concatenatedRule[ruleNumber]
        eBitValue=''
        for position in eBitPositionList:
            for pos in position:
                for p in pos:
                    # print(position, type(p))
                    eBitValue+=rule[p]
        rule+=' '+eBitValue
        if eBitValue in ruleSubsetFromEffectiveBit:
            ruleSubsetFromEffectiveBit[eBitValue].append('R'+str(ruleNumber))
        else:
            ruleSubsetFromEffectiveBit[eBitValue]=[]
            ruleSubsetFromEffectiveBit[eBitValue].append('R'+str(ruleNumber))
    #     print(rule)
    if printcommand=='withWildCard':
            print('withWildcard ')
            for k in ruleSubsetFromEffectiveBit:
                print(k,':',ruleSubsetFromEffectiveBit[k],len(ruleSubsetFromEffectiveBit[k]))
            print("_______________________")

    elif printcommand=='withOutWildCard':
            print('withOutWildcard ')
            for k in ruleSubsetFromEffectiveBit:
                print(k,':',ruleSubsetFromEffectiveBit[k],len(ruleSubsetFromEffectiveBit[k]))
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

    ruleNumbersToverifyDuplicate=ruleNumbersToverify[:]
    for ruleNo in ruleNumbersToverify:
        for k in ruleSubsetFromEffectiveBit:
            if ruleNo in ruleSubsetFromEffectiveBit[k]:
                # value+=1
                ruleNumbersToverifyDuplicate.remove(ruleNo)


    print('Total rules after Checking= ', ruleNumbersToverifyDuplicate)
    if len(ruleNumbersToverifyDuplicate)==0:
        print('#######Verified+Good#########')
    else:
        print('*********Fishy*********')

def findingSamplePosition(fileLoc,cb5tupleTable,fieldBitSize):
    # allfieldsTable=[]
    # concatenatedRule=[]
    rulesetNum=len(cb5tupleTable)
    allfieldsRule=createRuleList(cb5tupleTable)
    allfieldsTable=cb5tupleTable[:]
    concatenatedRule=allfieldsRule[:]
    bitCharTable=checkBitChr(allfieldsTable,fieldBitSize)
    fieldWC=getFieldWC(bitCharTable) #fieldWC[field]
    pos4SMatrix=pickPos4SMatrix(bitCharTable) #pos4SMatrix[field]
    similarityMatrix=getSimilarityMatrix(pos4SMatrix,allfieldsTable,fieldBitSize) #similarityMatrix[field][bit]
    for indexSize in range(0,1):
        print(fileLoc,rulesetNum, indexSize)
        bitPosCandidateList=getBitPosCandidateList(fieldWC,fieldBitSize,bitCharTable,similarityMatrix,cFactor)
        print('candidate= ',bitPosCandidateList,len(bitPosCandidateList),len(bitPosCandidateList[0]))
        fieldWCDiff=createFWCDiff(fieldWC)
        fieldReplaceList=createFieldReplaceList(fieldWCDiff,bitPosCandidateList,bitspaceSize)
        samplePositionCalculated=sorted(createSamplePos(bitPosCandidateList,fieldReplaceList,bitspaceSize,fieldPosition))
        samplePos=[]
        #samplePos.append(oldSmaplePos)
        samplePos.append(samplePositionCalculated)
        print('samplePositions= ', samplePos)
    return samplePos

# tSubsetLookup=[]
fwrite=open('Rules'+'_'+'effectiveBits_test','w')
for i in range(len(cbFileName)):
    fileLoc=cbFileName[i]
    # print(fileLoc)
    # fileLoc='acl3_1K'
    # allfieldsTable=[]
    # concatenatedRule=[]
    print('withWildcard')
    cb5tupleTable=loadClassBenchRuleFile(fileLoc,fieldBitSize)
    rulesetNum=len(cb5tupleTable)
    allfieldsRule=createRuleList(cb5tupleTable)
    allfieldsTable=cb5tupleTable[:]
    concatenatedRule=allfieldsRule[:]
    bitCharTable=checkBitChr(allfieldsTable,fieldBitSize)
    fieldWC=getFieldWC(bitCharTable) #fieldWC[field]
    pos4SMatrix=pickPos4SMatrix(bitCharTable) #pos4SMatrix[field]
    similarityMatrix=getSimilarityMatrix(pos4SMatrix,allfieldsTable,fieldBitSize) #similarityMatrix[field][bit]
    for indexSize in range(0,1):
        print(fileLoc,rulesetNum, indexSize)
        bitPosCandidateList=getBitPosCandidateList(fieldWC,fieldBitSize,bitCharTable,similarityMatrix,cFactor)
        print('candidate= ',bitPosCandidateList,len(bitPosCandidateList),len(bitPosCandidateList[0]))
        fieldWCDiff=createFWCDiff(fieldWC)
        fieldReplaceList=createFieldReplaceList(fieldWCDiff,bitPosCandidateList,bitspaceSize)
        samplePositionCalculated=sorted(createSamplePos(bitPosCandidateList,fieldReplaceList,bitspaceSize,fieldPosition))
        samplePos=[]
        #samplePos.append(oldSmaplePos)
        samplePos.append(samplePositionCalculated)
        print('samplePositions= ', samplePos)
    # samplePos=findingSamplePosition(fileLoc,cb5tupleTable,fieldBitSize)
    finalRules=rulesWithoutWildCardBits(fileLoc,fieldBitSize)
    print('withOutWildcard')
    samplePos1=findingSamplePosition(fileLoc,finalRules,fieldBitSize)
    verificationOfRuleset(cb5tupleTable,samplePos,'withWildCard')
    verificationOfRuleset(finalRules,samplePos,'withOutWildCard')
    verificationOfRuleset(finalRules,samplePos1,'withOutWildCard')
    verificationOfRuleset(cb5tupleTable,samplePos1,'withWildCard')

    allfieldsRuleWithOutWildCard=createRuleList(finalRules)
    # print(len(allfieldsRuleWithOutWildCard))
    # finalRules.append([])
    allfieldsRuleWithOutWildCard.append(samplePos[0][0])
    # print('ruleList',allfieldsRuleWithOutWildCard)
    for k in allfieldsRuleWithOutWildCard:
        fwrite.write(str(k)+'\n')

fwrite.close()
