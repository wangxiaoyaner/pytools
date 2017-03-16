import os.path
import fnmatch
import shutil
import os
import cv2

startFrame = 30
mol = 30
jpegTrain = ''
jpegTest = ''

def seq2jpgs(filepath, savepath):
	f = open(filepath, 'rb')
	string = str(f.read())
	splitstring = "\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46"
  	  # split .seq file into segment with the image prefix
    	strlist=string.split(splitstring)
  	f.close()
	
	numImg = len(strlist)


