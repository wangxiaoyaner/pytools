#实验结果记录
##ex_1:ZF+INRIA
忽略训练集中的所有负样本，只使用正样本进行训练
##ex_2:ZF+INRIA
把Anchor的比例改变，较第一次实验结果略有提升
##ex_3:ZF+Caltech Pedestrian Dataset
一开始一直没能收敛，后发现生成xml的时候将所有的非person标签标成了person，所以就呵呵了，后来试验出来了，mAP的算法正确率很低，意料之中。

>###待做：
* 完成实验的评价相关图像
* 使用VGG进行训练
* 改进Anchor的比例进行训练

