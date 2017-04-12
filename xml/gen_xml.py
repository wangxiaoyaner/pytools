#coding=utf-8
from xml.dom.minidom import Document
import re
import anno_class as anno
import os
import sys
import cv2
import argparse
_anno_dir = '/data/Caltech/annos/traintxts3'
_xml_dir =  '/data/Caltech/xml/Train3'
_jpeg_dir = '/data/Caltech/Train3'
_mode = 1
_diffcult = 0
def parse_args():
	'''
	Parse input arguments
	'''
        parser = argparse.ArgumentParser(description = 'gen xml annotations')
        parser.add_argument('--difficult', dest='difficult', help='wrapper image', default = 0, type = int)
	parser.add_argument('--annodir', dest='anno_dir', help='like pascal anno, jpeg, caltech anno txt', 
				default=_anno_dir, type=str)
	parser.add_argument('--xmldir', dest='xml_dir', help='path to save xml files',
				default=_xml_dir, type=str)
	parser.add_argument('--mode', dest='mode', help='0:only jpeg, 1:caltech txt, 2:pascal txt',
				default=_mode, type=int)
	parser.add_argument('--jpegdir', dest='jpeg_dir', help='if mode = 1, need the origin jpeg for more details',
				default=_jpeg_dir, type=str)
    #if len(sys.argv) == 1:
#		parser.print_help()
#		sys.exit(1)
	
	args = parser.parse_args()
	return args


def gen_node_with_text(doc, father, sunname, sun_text):
	sun = doc.createElement(sunname)
	father.appendChild(sun)
	sun.appendChild(doc.createTextNode(sun_text))
	return sun

def gen_just_node(doc, father, sunname):
	sun = doc.createElement(sunname)
	father.appendChild(sun)
	return sun
	
def write_info_to_xml(dir_file, AnnotationIf):
	folder_info = 'Caltech Pedestrain'
	filename_info = AnnotationIf.record.imgname
        filename_info = filename_info.split('.')[0]+'.jpg'
	database_info = 'Caltech Pedestrain'#AnnotationIf.record.database
	annotation_info = 'WXY annonation'
	image_info = 'null'
	source_flickrid_info = 'null'
	owner_flickrid_info = 'null'
	owner_name_info = 'null'
	width_info = AnnotationIf.record.weight
	height_info = AnnotationIf.record.height
	depth_info = AnnotationIf.record.depth
	segmented_info = str(0)

	
	doc = Document()
#根节点
	annotation = gen_just_node(doc,doc,'annotation')
#<folder>
	folder = gen_node_with_text(doc,annotation,'folder',folder_info)
#<filename>	
	filename = gen_node_with_text(doc, annotation,'filename', filename_info)
#<source>
	source = gen_just_node(doc, annotation, 'source')	
	#<database>
	database = gen_node_with_text(doc, source, 'database', database_info)
	#<annotation>
	anno = gen_node_with_text(doc, source, 'annotation', annotation_info)
	#<image>
	image = gen_node_with_text(doc, source, 'image', image_info)
	#<flickrid>
	source_flickrid = gen_node_with_text(doc, source, 'flickrid', source_flickrid_info)
#<owner>
	owner = gen_just_node(doc, annotation, 'owner')
	#<flickrid>
	owner_flickrid = gen_node_with_text(doc, owner, 'flickrid', owner_flickrid_info)
	#<name>
	owner_name = gen_node_with_text(doc, owner, 'name', owner_name_info)
#<size>
	size = gen_just_node(doc, annotation, 'size')
	#<width,height,depth>
	width = gen_node_with_text(doc, size, 'width', width_info)
	height = gen_node_with_text(doc, size, 'height', height_info)
	depth = gen_node_with_text(doc, size, 'depth', depth_info)
#<segmented>
	segmented = gen_node_with_text(doc, annotation, 'segmented', segmented_info)
	
	num_obj = len(AnnotationIf.record.xmin)
	for i in range(num_obj):
#<object>       
                if AnnotationIf.record.originlabel[i] == 'person':
		        mobject = gen_just_node(doc, annotation, 'object')
		#<name>
		        object_name = gen_node_with_text(doc, mobject, 'name', AnnotationIf.record.originlabel[i])
		#<pose,truncated,difficult>
		        object_pose = gen_node_with_text(doc, mobject, 'pose', 'UprightPerson')
	        	object_truncated = gen_node_with_text(doc, mobject, 'truncated', '0')
                        diff = float(AnnotationIf.record.ymax[i]) - float(AnnotationIf.record.ymin[i])
                        if _diffcult == 1 and diff < 50:
                                diff = 1
                        else:
                                diff = 0
	        	object_difficult = gen_node_with_text(doc, mobject, 'difficult', str(diff))
		#<bndbox>
	        	object_bndbox = gen_just_node(doc, mobject, 'bndbox')
		#<xmin,ymin,xmax,ymax>
	        	xmin = gen_node_with_text(doc, object_bndbox, 'xmin', AnnotationIf.record.xmin[i])
	        	ymin = gen_node_with_text(doc, object_bndbox, 'ymin', AnnotationIf.record.ymin[i])
	            	xmax = gen_node_with_text(doc, object_bndbox, 'xmax', AnnotationIf.record.xmax[i])
		        ymax = gen_node_with_text(doc, object_bndbox, 'ymax', AnnotationIf.record.ymax[i])
	#
        
	with open(dir_file, 'w') as f:
		f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))
	return 
def main():
	args = parse_args()
        pac_anno_dir = args.anno_dir
        xml_anno_dir = args.xml_dir
        mode = args.mode
        _diffcult = args.difficult
	caltech_jpeg_dir = args.jpeg_dir
	#给jpeg图像弄个xml
	if int(mode) == 0:
                for file in os.listdir(pac_anno_dir):
                        if file.endswith(".jpg"):
                              #  print file
                                myanno = anno.AnnotationInfo()
                                myanno.handle_jpeg(os.path.join(pac_anno_dir, file))
                                write_info_to_xml(os.path.join(xml_anno_dir, file[0:len(file)-4]+".xml"), myanno)
                return
        if mode == 1:
		for txt in os.listdir(pac_anno_dir):
		        reans = re.match(r'(\d+)\.txt',txt)
			if reans:
		                jpegn = reans.group(1)+'.jpg'
				jpegname = os.path.join(caltech_jpeg_dir, jpegn)
				myanno = anno.AnnotationInfo()
				myanno.handle_caltech_txt(os.path.join(pac_anno_dir,txt), jpegname)
				write_info_to_xml(os.path.join(xml_anno_dir,reans.group(1) + '.xml'), myanno)
		return




	#给pascal文件弄个xml
        for file in os.listdir(pac_anno_dir):
                if file.endswith(".txt"):
	                myanno = anno.AnnotationInfo()
	                myanno.handle_pascal_txt(os.path.join(pac_anno_dir, file))
                        write_info_to_xml(os.path.join(xml_anno_dir,file[0:len(file)-4]+".xml"), myanno)

if __name__=="__main__":
	main()
