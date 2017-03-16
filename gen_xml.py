#coding=utf-8
from xml.dom.minidom import Document
import anno_class as anno
import os
import sys
import cv2

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
	folder_info = 'INRIA'
	filename_info = AnnotationIf.record.imgname
        filename_info = filename_info.split('.')[0]+'.jpg'
	database_info = 'INRIA'#AnnotationIf.record.database
	annotation_info = 'PASCAL Annotation Version 1.00'
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
		mobject = gen_just_node(doc, annotation, 'object')
		#<name>
		object_name = gen_node_with_text(doc, mobject, 'name', 'person')
		#<pose,truncated,difficult>
		object_pose = gen_node_with_text(doc, mobject, 'pose', 'UprightPerson')
		object_truncated = gen_node_with_text(doc, mobject, 'truncated', '0')
		object_difficult = gen_node_with_text(doc, mobject, 'difficult', '0')
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
        pac_anno_dir = sys.argv[1]
        xml_anno_dir = sys.argv[2]
        mode = sys.argv[3]
        if int(mode) == 0:
                for file in os.listdir(pac_anno_dir):
                        if file.endswith(".jpg"):
                              #  print file
                                myanno = anno.AnnotationInfo()
                                myanno.handle_jpeg(os.path.join(pac_anno_dir, file))
                                write_info_to_xml(os.path.join(xml_anno_dir, file[0:len(file)-4]+".xml"), myanno)
                return
                
        for file in os.listdir(pac_anno_dir):
                if file.endswith(".txt"):
	                myanno = anno.AnnotationInfo()
	                myanno.handle_pascal_txt(os.path.join(pac_anno_dir, file))
                        write_info_to_xml(os.path.join(xml_anno_dir,file[0:len(file)-4]+".xml"), myanno)

if __name__=="__main__":
	main()
