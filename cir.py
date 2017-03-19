#coding = utf-8
import matplotlib.pyplot as plt
import re
class caffeloss:
    def __init__(self):
        self.bbox_loss = []
        self.cls_loss = []
        self.rpn_cls_loss = []
        self.rpn_loss_bbox = []
        self.iter = []
        self.lr = []
        self.p1 = re.compile(r'Iteration (\d+), lr = (\d+\.\d+)')
        self.pbbox_loss = re.compile(r'Train net output #0: bbox_loss = ((nan)|(\d+\.\d+))')
        self.pcls_loss = re.compile(r'Train net output #1: cls_loss = ((nan)|(\d+\.\d+))')
        self.prpn_cls_loss = re.compile(r'Train net output #2 rpn_cls_loss = ((nan)|(\d+\.\d+))')
        self.prpn_loss_bbox = re.compile(r'Train net output #3 rpn_loss_bbox= ((nan)|(\d+\.\d+))')

        
    def match_mode(self, line):
        match = self.p1.match(line)
        if match:
            self.iter.append(int(match.group(1)))
            self.lr.append(float(match.group(2)))
            return
        match = self.pbbox_loss.match(line)
        if match:
            bbloss = match.group(1)
            if bbloss == 'nan':
                bblos = 65535.0
            else:
                bblos = float(match.group(1))
            return
        match = self.pcls_loss.match(line)
        if match:
            clsloss = match.group(1)
            if clsloss == 'nan':
                clsloss = 65535.0
            else:
                clsloss = float(match.group(1))
            return 
        match = self.prpn_cls_loss.match(line)
        if match:
            tmp = match.group(1)
            if tmp == 'nan':
                tmp = 65535.0
            else:
                tmp = float(match.group(1))
            return 
        match = self.prpn_loss_bbox.match(line)
        if match:
            tmp = match.group(1)
            if tmp == 'nan':
                tmp = 65535.0
            else:
                tmp = float(match.group(1))
                
            return
    def plot_img(self):
        

