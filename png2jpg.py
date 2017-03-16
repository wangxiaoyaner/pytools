import os
import sys
import cv2
dirname = sys.argv[1]
for file in os.listdir(dirname):
	if file.endswith(".png") or file.endswith("jpg"):
		newname = file[0:len(file)-4] + ".jpg"
		oldname = os.path.join(dirname,file)
		img = cv2.imread(oldname)
		newname = os.path.join(dirname,newname)
		print oldname,newname
		os.rename(oldname,newname)
		cv2.imwrite(newname,img)
