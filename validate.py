
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

def readFile(fileName):
    fop=open(fileName,'r')
    tempData=fop.readlines()
    fop.close()
    tempDataNoCarrigeReturn=[]
    bitPositionList=[]
    bitpositionListFinal=[]
    for i in tempData:
        tempDataNoCarrigeReturn.append(i.replace('\n',' '))
    for i in tempDataNoCarrigeReturn:
        bitpositions=i.replace(' ','').replace('[','').replace(']','').split(',')
        bitPositionList.append(bitpositions)
    for i in bitPositionList:
        pos=[]
        for k in i:
            pos.append(int(k))
        bitpositionListFinal.append(pos)
    return bitpositionListFinal

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
        # for position in eBitPositionList:
        #     for pos in position:
        for p in eBitPositionList:
                    # print(position, type(p))
            eBitValue+=rule[p]
        rule+=' '+eBitValue
        if eBitValue in ruleSubsetFromEffectiveBit:
            ruleSubsetFromEffectiveBit[eBitValue].append('R'+str(ruleNumber))
        else:
            ruleSubsetFromEffectiveBit[eBitValue]=[]
            ruleSubsetFromEffectiveBit[eBitValue].append('R'+str(ruleNumber))
    #     print(rule)
    if printcommand=='samplePositionOriginal':
            print('samplePositionOriginal', eBitPositionList)
            for k in ruleSubsetFromEffectiveBit:
                print(k,':',ruleSubsetFromEffectiveBit[k],len(ruleSubsetFromEffectiveBit[k]))
                print("_______________________")

    elif printcommand=='samplePositionPredicted':
            print('samplePositionPredicted',eBitPositionList)
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
        print('#######Verified+GoodShot#########')
    else:
        print('*********FishyChoices*********')
    return ruleSubsetFromEffectiveBit

cbFileName=[]
fieldBitSize=[32,32,16,16,8] # tuple5Size=[32,32,16,16,8]
for i in range(0,100):
    filename='acl1_1k_'+str(i)
    cbFileName.append(filename)
# cbFileName=[]
# print(cbFileName,len(cbFileName))
samplePositionoriginal=readFile('effectiveBitsSetsOriginal')
samplePositionPredicted=readFile('effectiveBitsSetsPredicted')
# print(samplePositionoriginal,len(samplePositionoriginal))
# print(samplePositionPredicted,len(samplePositionPredicted))
print('**********************')
print('######################')
print('%%%%%%%%%%%%%%%%%%%%%%')
totalGroupsOriginal=[]
totalGroupsPredicted=[]
for i in range(len(cbFileName)):
    fileLoc=cbFileName[i]
    print(fileLoc)
    cb5tupleTable=loadClassBenchRuleFile(fileLoc,fieldBitSize)
    ruleGroupesFromOri= verificationOfRuleset(cb5tupleTable,samplePositionoriginal[i],'samplePositionOriginal')
    ruleGroupesFromPre=verificationOfRuleset(cb5tupleTable,samplePositionPredicted[i],'samplePositionPredicted')
    totalGroupsOriginal.append(ruleGroupesFromOri)
    totalGroupsPredicted.append(ruleGroupesFromPre)
summaryOriginal=[]
summaryPredicted=[]
noOfRulesPerSet=10
#summaryValue= [no of groups, max number of rules in a group, rule number, NBinth=maxNoRules/(numofRules/numberOf Groups)]
for dictOriginal in totalGroupsOriginal:
    summaryValue=[]
    summaryValue.append(len(dictOriginal.keys()))
    ruleNumbers=lambda x: len(dictOriginal[x])
    rulePerGroup=[]
    for i in dictOriginal:
        rulePerGroup.append(ruleNumbers(i))
    maxbinth=max(rulePerGroup)
    summaryValue.append(maxbinth)
    nBinth=(maxbinth)/(noOfRulesPerSet/len(dictOriginal.keys()))
    summaryValue.append(nBinth)
    summaryOriginal.append(summaryValue)

for dictPredicted in totalGroupsPredicted:
    summaryValue=[]
    summaryValue.append(len(dictPredicted.keys()))
    ruleNumbers=lambda x: len(dictPredicted[x])
    rulePerGroup=[]
    for i in dictPredicted:
        rulePerGroup.append(ruleNumbers(i))
    maxbinth=max(rulePerGroup)
    summaryValue.append(maxbinth)
    nBinth=(maxbinth)/(noOfRulesPerSet/len(dictPredicted.keys()))
    summaryValue.append(nBinth)
    summaryPredicted.append(summaryValue)


for i in range(len(summaryPredicted)):
    print('NNPredicted: Ruleset'+str(i))
    print('TotalGroups=',summaryPredicted[i][0],
          'maxbinth= ',summaryPredicted[i][1],
          'noofRules= ', noOfRulesPerSet,
          'Normalizedbinth= ', summaryPredicted[i][2])
    print('------------------------------')
    print('3MetricCalculated: Ruleset'+str(i))
    print('TotalGroups=',summaryOriginal[i][0],
          'maxbinth= ',summaryOriginal[i][1],
          'noofRules= ', noOfRulesPerSet,
          'Normalizedbinth= ', summaryOriginal[i][2])
    print('################################')
