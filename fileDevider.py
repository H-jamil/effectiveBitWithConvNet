
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

fileDevider('acl1_1k')
