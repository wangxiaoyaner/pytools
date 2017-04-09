#coding=utf-8

'''
input detections.pkl
input test.txt give name info
output caltech stardard detection format
'''

import numpy as np
import os
import cPickle

data_path = "USA_data/res/OurMethod"
set_path=["set06","set07","set08","set09","set10"]

#make_dir
for i in set_path:
    if os.path.exists(os.path.join(data_path,i)):
        continue
    os.mkdir(os.path.join(data_path,i))

with open(os.path.join(data_path,'test.txt'),'rb') as f:
    item = f.readlines()
    setId = ['set'+i[0:2] for i in item]
    volId = ['V'+i[2:5]+'.txt' for i in  item]
    frameId = [int(i[6:11]) for i in item]
    
dt_path = os.path.join(data_path,'detections.pkl')
assert os.path.exists(dt_path)

with open(dt_path,'rb') as f:
    dt = cPickle.load(f)
    assert len(dt) == 2
    dt = dt[1]
    assert len(dt) == 4024
    assert len(frameId) == 4024
    nvolid = volId[0]
    nsetid = setId[0]
    now_path = os.path.join(data_path,nsetid,nvolid)
    now_file = open(now_path,'w')
    for i in range(len(dt)):
        if nvolid != volId[i]:
    #        np.savetxt(os.path.join(data_path,nsetid,nvolid),tmp,fmt="%s",newline='\n')
            now_file.close()
            nvolid = volId[i]
            nsetid = setId[i]
            now_path = os.path.join(data_path, nsetid, nvolid)
            now_file = open(now_path,'w')

        s1 = dt[i][:,0:2]
        s2 = dt[i][:,2]-dt[i][:,0]
        s3 = dt[i][:,3]-dt[i][:,1]
        s4 = dt[i][:,4]
        s2 = s2.reshape(len(s2),1)
        s3 = s3.reshape(len(s3),1)
        s4 = s4.reshape(len(s4),1)
        s0 = np.zeros((len(s4),1))
        assert len(s0) == len(s1)
        s0[:,0] = frameId[i]
        sdt = np.hstack((s0,s1,s2,s3,s4))
        for j in sdt:
            now_file.write('{} {} {} {} {} {}\n'.format(int(j[0]),j[1],j[2],j[3],j[4],j[5]))



 
