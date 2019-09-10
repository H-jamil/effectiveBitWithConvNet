import os
def fileDevider(filename):
    rulePerFile=10
    fop=open(filename,'r')
    tempData=fop.readlines()
    fop.close()
    totalRules=len(tempData)
    totalStep=int(totalRules/rulePerFile)
    start=0
    step=rulePerFile
    for i in range (totalStep):
        writeList=tempData[start:start+step]
        fwrite=open(filename+'_'+str(i),'w')
        for k in writeList:
            fwrite.write(str(k))
        fwrite.close()
        start+=step
cwd=os.getcwd()
fileDevider('acl1_100k')
list1 = os.listdir(cwd)
print(list1)
