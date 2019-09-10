import numpy as np
import sys
import keras.backend as K
import math
# import numpy as np
import h5py
import matplotlib.pyplot as plt
np.set_printoptions(threshold=sys.maxsize)
ruleSetSize=10

def readFile(fileName):
    fop=open(fileName,'r')
    tempData=fop.readlines()
    fop.close()
    tempDataNoCarrigeReturn=[]
    for i in tempData:
        tempDataNoCarrigeReturn.append(i.replace('\n',' '))
    return tempDataNoCarrigeReturn

def rulesWithOutputLayer(tempData):
    tempDatawithOutputLayer=[]
    initialRulesetIndex=0
    for i in range(len(tempData)):
        if i==initialRulesetIndex+ruleSetSize:
            initialRulesetIndex=i+1
            # print('tempData',tempData[i])
            value=tempData[i][1:-2]
            # print ('value',value)
            bitPositions=value.replace(' ','').split(',')
            # print('bitpositions',bitPositions)
            outLayerValue=''
            for index in range(0,104):
                if str(index) in bitPositions:
                    outLayerValue+='1'
                else:
                     outLayerValue+='0'
            # print('outLayerValue', outLayerValue, len(outLayerValue))
            tempDatawithOutputLayer.append(outLayerValue)
        else:
            tempDatawithOutputLayer.append(tempData[i][:-1])
    return tempDatawithOutputLayer

tempData=readFile('Rules_effectiveBits')
tempDatawithOutputLayer=rulesWithOutputLayer(tempData)


#for test DataSet

tempData1=readFile('testRules_effectiveBits')
tempDatawithOutputLayer1=rulesWithOutputLayer(tempData1)

# rulesetArray=np.zeros((104,1))
# print(rulesetArray)
def loadDataset():
    ruleListAll=[]
    outputListAll=[]
    numberOfRuleset=0
    startIndex=0
    stopIndex=startIndex+ruleSetSize
    print('#################### Training')
    i=0
    for i in range(0,len(tempDatawithOutputLayer),ruleSetSize):
        ruleList=[]
        for k in range (startIndex,stopIndex):
            npArray=np.array(list(tempDatawithOutputLayer[k]),dtype=int)
            npArray=npArray.reshape(104,1)
            ruleList.append(npArray)
        # print("done")
        numberOfRuleset+=1
        npArray=np.array(list(tempDatawithOutputLayer[stopIndex]),dtype=int)
        npArray=npArray.reshape(104,1)
        outputListAll.append(npArray)
        i=stopIndex
        startIndex=stopIndex+1
        stopIndex=startIndex+ruleSetSize
        rulesetArray=np.stack(ruleList,axis=0)
        ruleListAll.append(rulesetArray)
        if stopIndex>=len(tempDatawithOutputLayer):
            break
        # print(npArray,npArray.shape )
        # rulesetArray=np.stack(npArray,axis=1)
    ruleListAllArray=np.stack(ruleListAll,axis=0)
    ouputListALlArray=np.stack(outputListAll,axis=0)
    # rulesetArray=np.stack(ruleList,axis=0)
    # print('ruleListAllArray',ruleListAllArray.shape)
    # print('numberOfRuleset', numberOfRuleset)
    # print('ouputListALlArray',ouputListALlArray.shape)
    # print(ruleListAllArray)

    return ruleListAllArray,ouputListALlArray

def testDataSet():
    ruleListAll=[]
    outputListAll=[]
    numberOfRuleset=0
    startIndex=0
    stopIndex=startIndex+ruleSetSize
    print('#################### Test')
    i=0
    for i in range(0,len(tempDatawithOutputLayer1),ruleSetSize):
        ruleList=[]
        for k in range (startIndex,stopIndex):
            npArray=np.array(list(tempDatawithOutputLayer1[k]),dtype=int)
            npArray=npArray.reshape(104,1)
            ruleList.append(npArray)
        # print("done")
        numberOfRuleset+=1
        npArray=np.array(list(tempDatawithOutputLayer1[stopIndex]),dtype=int)
        npArray=npArray.reshape(104,1)
        outputListAll.append(npArray)
        i=stopIndex
        startIndex=stopIndex+1
        stopIndex=startIndex+ruleSetSize
        rulesetArray=np.stack(ruleList,axis=0)
        ruleListAll.append(rulesetArray)
        if stopIndex>=len(tempDatawithOutputLayer1):
            break
        # print(npArray,npArray.shape )
        # rulesetArray=np.stack(npArray,axis=1)
    ruleListAllArray=np.stack(ruleListAll,axis=0)
    ouputListALlArray=np.stack(outputListAll,axis=0)
    # rulesetArray=np.stack(ruleList,axis=0)
    # print('ruleListAllArray',ruleListAllArray.shape)
    # print('numberOfRuleset', numberOfRuleset)
    # print('ouputListALlArray',ouputListALlArray.shape)
    # print(ruleListAllArray)

    return ruleListAllArray,ouputListALlArray

# print(rulesetArray)
# print(ruleList[0].reshape(104,))
# print(rulesetArray[0].reshape(104,))
