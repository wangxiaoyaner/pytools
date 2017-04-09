#PAMI12Pedestrians
## py-faster-rcnn 源码阅读test.py
###关键函数：
```
scores, boxes = im_detect(net, im, box_proposals=None)net是caffe里的Net
_get_image_blob(im)把图像转化为一个网络的输入
要给像素减去均值
根据TEST的图像尺寸，resize, blob：(batch ele, channel, height, width)
巴拉巴拉就去预测了，
测试后取了roi和prob
但是还要取得回归器的参数并进行bbox reg
最后得到了校正后的bb和score
简单的做一下阈值处理
然后把他进行nms（阈值初始是0.3）
之后把每张图片的检测图片控制在100个
每张图片最多保留 一百个检测结果
all_box被存在detection的
detection:
把一个cls的结果放到一个txt文件里，然后调用do_python_eval函数
do_python_eval里有个
rec,prec,ap = voc_eval(filename, annopath, imagesetfile, cls, cachedir, ovthresh=0.5)
显示准备annos放在recs[gt]里，每个item都是一张图片{name, pose, truncated, difficult, box}的一个集合
读检测结果的额文件，提取每个bbox的图片，得分，bbox并根据得分降序排列

因为是rpn方法啦
```
cv2.resize(interpolation=CV2.INTER_LINEAR)
blob{'data',(id,channel, height, width), 'roios', 'im_info'(height,weight,im_scale,np.float32)

###关于评价方法。
这里的AP是precision, recall曲线下方的面积。在代码中，按照得分由高到低分别记录每个预测框的属性，通过fp[]和tp[],通过对应id的下标是0还是1标注。然后计算累积的recall和precision。控制的方法就是选前多少个预测框进行计算。
而voc_ap函数就是计算曲线下方面积的方法。


difficult是用来标记你不想用到的gt_box的很实用，这里我们生成test的xml标注的时候可以设定一下评价的区间。
## 3. EVALUATION METHODOLOGY

在网站上有评价代码，GT annotations以及各种检测器在各种检测集合上的检测结果。这样保证比较的可复制性。总之，这样很好，我们还升级了测试方法。

### 3.1 Full Image Evalution
对单帧图像检测，检测系统输入一张图，返回一堆检测（BB,score)。系统进行多尺度检测，以及必要的非极大值抑制。最后的结果是a list of BB。

BB_dt和BB_gt是否匹配，通过PASCAL 方式。交并比a_o超过0.5.
一旦交并比阈值低于0.6， 这个结果就就变得敏感了。我了好点的检测，我们把他定在了0.5上。
每个BB_dt和BB_gt至多匹配一次。通过**贪婪**算法消除歧义。先把高分的进行匹配。然后找交并比最高的gt进行匹配。
这样下来，不匹配的BB_dt是错误正例。没匹配的BBGT是错误的负例。