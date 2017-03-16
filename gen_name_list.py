import os
import sys
dirname = sys.argv[1]
filename =sys.argv[2]
mode = sys.argv[3]
f = open(filename,mode)
for file in os.listdir(dirname):
	if file.endswith(".jpg"):
		newname = file[0:len(file)-4]
		f.write(newname+'\n')
f.close()
