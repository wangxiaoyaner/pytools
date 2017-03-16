import re
import cv2
import gen_xml as gen
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
                self.caltech3 = re.compile(r'pos: (\d+
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
	
        def match_caltech_mode(self, line):
                
	def handle_pascal_txt(self, pastxt):
		f = open(pastxt, 'r')
		lines = f.readlines()
		f.close()
		for line in lines:
			self.match_mode(line)
        def handle_kitti_txt(self, kitti_txt):
                pass
        def handle_caltech_txt(self, caltech_txt), jpeg):
                img = cv2.imread(jpeg)
                self.record.height = str(img.shape[0])
                self.record.weight = str(img.shape[1])
                self.record.depth = str(img.shape[2])
                tmp = jpeg.split('/')
                self.record.imgname = tmp[len(tmp)-1]
                f = open(caltech_txt, 'r')
                lines = f.readlines()
                f.close()

            
        def handle_jpeg(self, jpeg):
                img = cv2.imread(jpeg)
                self.record.height = str(img.shape[0])
                self.record.weight = str(img.shape[1])
                self.record.depth = str(img.shape[2])
                tmp = jpeg.split('/')
                self.record.imgname = tmp[len(tmp)-1]
