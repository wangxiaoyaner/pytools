import os.path
import fnmatch
import os
import cv2
import re

startFrame = 30
mol = 30
jpegTrain = '/data/Caltech/Train'
jpegTest = '/data/Caltech/Test'
setdir = '/data/Caltech/caltech/'
trainset = ['set00','set01','set02','set03','set04','set05']
testset = ['set06', 'set07', 'set08', 'set09', 'set10']
checklog = '/data/check.txt'
ckfid = open(checklog, 'w')
def seq2jpgs(filepath, savepath):
    f = open(filepath, 'rb')
    string = str(f.read())
    splitstring = "\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46"
    strlist = string.split(splitstring)
    f.close
    
    reans = re.match(r'.*set(\d\d).*V(\d\d\d).*', filepath)
    setid = reans.group(1)
    vid = reans.group(2)
    iid = '000000'
        
    i = startFrame
    seqlen = len(strlist) - 1
    ckfid.write(str(seqlen))
    ckfid.write('\n')

    while i <= seqlen:
        name = iid + str(i)
        name = name[len(name)-6:len(name)]
        name = setid + vid + name + '.jpg'
        name = os.path.join(savepath, name)
        print name
        f = open(name, 'wb')
        f.write(splitstring)
        f.write(strlist[i])
        f.close()
        i = i+mol

if __name__ == "__main__":
    for train_item in trainset:
        p1 = os.path.join(setdir, train_item)
        for parent,dirnames, filenames in os.walk(p1):
            for filename in filenames:
                if filename[0] != '.':
                    p2 = os.path.join(p1, filename)
                    seq2jpgs(p2,jpegTrain)


    for test_item in testset:
        p1 = os.path.join(setdir, test_item)
        for parent, dirnames, filenames in os.walk(p1):
            for filename in filenames:
                if filename[0] != '.':
                    p2 = os.path.join(p1, filename)
                    seq2jpgs(p2,jpegTest)

    ckfid.close()
        
    

