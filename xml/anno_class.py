#coding=utf-8
import re
import cv2
class PASemptyrecord:
	def __init__(self):
		self.imgname = ''
		self.weight = ''
		self.height = ''
		self.depth = ''
		self.database = ''
		self.xmin = []
		self.ymin = []
		self.xmax = []
		self.ymax = []
                self.vxmin = []
                self.vymin = []
                self.vxmax = []
                self.vymax = []
                self.occl = []
                self.lock = []
		self.originlabel = []
class AnnotationInfo:
	def __init__(self):
		self.record = PASemptyrecord()
		self.pattern1 = re.compile(r'Image filename : "(.+)"')
		self.pattern2 = re.compile(r'Image size \(X x Y x C\) : (\d+) x (\d+) x (\d+)')
		self.pattern3 = re.compile(r'Database : "(.+)"')
		self.pattern4 = re.compile(r'Bounding box for object \d+ ".+" \(Xmin, Ymin\) - \(Xmax, Ymax\) : \((\d+), (\d+)\) - \((\d+), (\d+)\)')
		self.pattern5 = re.compile(r'Original label for object \d+ ".+" : "(.+)"')
                
		self.caltech1 = re.compile(r'num: (\d+)')
                self.caltech2 = re.compile(r'label: (.+)')
                self.caltech3 = re.compile(r'pos: (\d+\.\d+) (\d+\.\d+) (\d+\.\d+) (\d+\.\d+)')
		self.caltech4 = re.compile(r'occl: (\d+)')
		self.caltech5 = re.compile(r'lock: (\d+)')
		self.caltech6 = re.compile(r'posv: (\d+\.\d+) (\d+\.\d+) (\d+\.\d+) (\d+\.\d+)')

        def match_caltech_mode(self, line):
		match = self.caltech2.match(line)
		if match:
			tmp = match.group(1)
			self.record.originlabel.append(tmp)
			return

		match = self.caltech3.match(line)
		if match:
			posx1 = (float(match.group(1)))
			posy1 = (float(match.group(2)))
			posx2 = (float(match.group(3))) + posx1
			posy2 = (float(match.group(4))) + posy1
                        if posx2 >= int(self.record.weight):
                                print self.record.imgname, 'posx2', posx2,self.record.originlabel[-1], posx1, posy1, posx2,posy2
                                posx2 = 639
                        if posy2 >= int(self.record.height):
                                print self.record.imgname,'posy2',posy2, self.record.originlabel[-1], posx1, posy1, posx2, posy2
                                posy2 = 479
                        assert posx1 >= 0
                        assert posy1 >= 0
                        assert posx2 != 640
                        assert posy2 != 480
                        self.record.xmin.append(str(posx1))
			self.record.ymin.append(str(posy1))
			self.record.xmax.append(str(posx2))
			self.record.ymax.append(str(posy2))
                        
                            #print posx2, self.record.weight
                        #assert posx2 < int(self.record.weight)
                        #if float(match.group(3)) > float(match.group(4)) and cmp('person',self.record.originlabel[-1])==0:
                        #        print match.group(3), match.group(4),posx1,posy1,posx2,posy2
                        #        print self.record.imgname
			return
		match = self.caltech4.match(line)
		if match:
			self.record.occl.append(match.group(1))
			return
		match = self.caltech5.match(line)
		if match:
			self.record.lock.append(match.group(1))
			return
		match = self.caltech6.match(line)
		if match:
			posvx1 = float(match.group(1))
			posvy1 = float(match.group(2))
			posvx2 = float(match.group(3)) + posvx1
			posvy2 = float(match.group(4)) + posvy1
			self.record.vxmin.append(str(((posvx1))))
			self.record.vymin.append(str(((posvy1))))
			self.record.vxmax.append(str(((posvx2))))
			self.record.vymax.append(str(((posvy2))))
			return
			

	def match_mode(self,line):
		match = self.pattern1.match(line)
		if match:
			tmp = match.group(1)
                        self.record.imgname = tmp[len(tmp)-1]
			return 

		match = self.pattern2.match(line)
		if match:
			self.record.weight = match.group(1)
			self.record.height = match.group(2)
			self.record.depth = match.group(3)
			return

		match = self.pattern3.match(line)
		if match:
			self.record.database = match.group(1)
			return

		match = self.pattern4.match(line)
		if match:
			self.record.xmin.append(match.group(1))
			self.record.ymin.append(match.group(2))
			self.record.xmax.append(match.group(3))
			self.record.ymax.append(match.group(4))
			return
		match = self.pattern5.match(line)
		if match:
			self.record.originlabel.append(match.group(1))
			return 
#		print 'ERROR, NO MACHES FOUND!'
	
	def handle_caltech_txt(self, caltech_txt, jpeg):
                img = cv2.imread(jpeg)
                self.record.height = str(img.shape[0])
                self.record.weight = str(img.shape[1])
                self.record.depth = str(img.shape[2])
                tmp = jpeg.split('/')
                self.record.imgname = tmp[len(tmp)-1]
                f = open(caltech_txt, 'r')
                lines = f.readlines()
                f.close()
		for line in lines:
			self.match_caltech_mode(line)

        
	def handle_pascal_txt(self, pastxt):
		f = open(pastxt, 'r')
		lines = f.readlines()
		f.close()
		for line in lines:
			self.match_mode(line)
        def handle_kitti_txt(self, kitti_txt):
                pass
            
        def handle_jpeg(self, jpeg):
                img = cv2.imread(jpeg)
                self.record.height = str(img.shape[0])
                self.record.weight = str(img.shape[1])
                self.record.depth = str(img.shape[2])
                tmp = jpeg.split('/')
                self.record.imgname = tmp[len(tmp)-1]
