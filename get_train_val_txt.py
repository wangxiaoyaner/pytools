import os
import sys
import random
source = sys.argv[1]
bili = sys.argv[2]
train_txt = open('train.txt', 'w')
val_txt = open('val.txt','w')
sfile = open(source, 'r')
ans = sfile.readlines()
val_num = int(round(len(ans)*float(bili)))
train_num = len(ans) - val_num
val_item = random.sample(ans, val_num)
for item in val_item:
	ans.remove(item)
for x in ans:
	print x
	train_txt.write(x)
for y in val_item:
	val_txt.write(y)
train_txt.close()
sfile.close()
val_txt.close()


