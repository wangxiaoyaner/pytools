#coding=utf-8
import numpy as np
import os
import math
import scipy.io as sio
import cPickle 

nframe_path = 'USA_data/nFrame_USA_anno/framesnum.txt'
ans_path = 'USA_data/res'
gt_path = 'USA_data/usa_anno_mat'
inf = float("inf")

class resEvalAlgs:
	pass

class EVALclatech:
	def __init__(self, framep, ansp):
		self.samples = 10.**np.arange(-2,0.2,.25) 
		self.lims = np.array([2e-4,50.000,0.0350,1.])
		assert os.path.exists(ans_path)
		self.frame_num_info = np.loadtxt(framep, dtype=int)
		self.ans = {}#dt
		self.res = []#list of resEvalAlgs,2D
		self.ans_path = ansp
		self.item = []
		self.debug = []
		self.gt = {}#gt
		self.gt_path = gt_path
		self.exps = [['Reasonable',[50,inf],[0.65,inf],0,0.5, 1.25],
			['All', [20,inf],[.2,inf],0, .5,1.25],
  			['Scale=near',     [80,inf],  [inf,inf], 0,   .5,  1.25],
  			['Scale=medium',   [30,80],   [inf,inf], 0,   .5,  1.25],
  			['Scale=large',    [100,inf], [inf,inf], 0,   .5,  1.25],
 			['Scale=far',      [20,30],   [inf,inf], 0,   .5,  1.25]
			]#需要喝下面的一一对应
		#name, hr, vr, ar, overlap, filter
                self.resize={"CCF":0,"ACF++":0,"OurMethod":0}
		self.aspectRatio = 0.41
		self.ansevalalgs = []

	def compOas(self, dt, gt, ig):
		#computes overlap area between pairs of bbs
		m = dt.shape[0]
		n = gt.shape[0]
		oa = np.zeros((m,n))
		
		de = dt[:,0:2] + dt[:,2:4]
		da = dt[:,2] * dt[:,3]
		ge = gt[:,0:2] + gt[:,2:4]
		ga = gt[:,2] * gt[:,3]
		for  i in range(m):
			for j in range(n):
				w = min(de[i,0],ge[j,0])-max(dt[i,0],gt[j,0])
				if w <= 0:
					continue
				h = min(de[i,1],ge[j,1])-max(dt[i,1],gt[j,1])
				if h <= 0:
					continue

				t = w*h
				if (ig[j]):
					u = da[i]
				else:
					u = da[i]+ga[j]-t
				oa[i,j] = t/u
		return oa

	def evalResmini(self, gtnp, dtnp, thr = 0.5, mul = 0):
		if len(gtnp) == 0:
			gtnp = np.zeros([0,5])
		if len(dtnp) == 0:
			dtnp = np.zeros([0,5])
		assert dtnp.shape[1] == 5
		assert gtnp.shape[1] == 5
		nd = dtnp.shape[0]
		ng = gtnp.shape[0]
		gtnp = gtnp[np.argsort(gtnp[:,4]),:]
		dtnp = dtnp[np.argsort(-dtnp[:,4]),:]
		gt = gtnp
		gt[:,4]=-gt[:,4]
		dt = dtnp
		dt = np.hstack((dt,np.zeros((nd,1))))
		oa = self.compOas(dt[:,0:4], gt[:,0:4], gt[:,4]==-1)
		for d in range(nd):
			bst0a = thr
			bstg = 0
			bstm = 0
			for g in range(ng):
				m = gt[g,4]
				if m==1 and mul == 0:
					continue
				if(bstm != 0 and m == -1):
					break
				if(oa[d,g]<bst0a):
					continue
				bst0a= oa[d,g]
				bstg = g
				if m == 0:
					bstm = 1
				else:
					bstm = -1
			g = bstg
			m = bstm
			if m == -1:
				dt[d,5] = m
			elif m == 1:
				gt[g,4] = m
				dt[d,5] = m
		return gt,dt


	def evalRes(self, gt0, dt0, thr = 0.5, mul=0):
		assert len(gt0) == len(dt0)
		gt = range(len(gt0))
		dt = range(len(dt0))
		for i in range(len(gt0)):
			[gt[i],dt[i]] = self.evalResmini(gt0[i],dt0[i],thr,mul)

		return gt,dt



	def evalAlgs(self, gts, dts):
		for i in range(len(gts)):
			gt = gts[i]
			self.res.append([])
			for j in range(len(dts)):
				dt = dts[j]
				res = resEvalAlgs()
				res.stre = self.exps[i][0]
				res.stra = self.resize.keys()[j]
				hr = np.array(self.exps[i][1]) * np.array([1/self.exps[i][5],self.exps[i][5]])
				print hr
				for b in range(len(dt)):
					dt[b] = dt[b][np.where(dt[b][:,3]>=hr[0])[0],:]
					dt[b] = dt[b][np.where(dt[b][:,3]<hr[1])[0],:]

				[gtr, dtr] = self.evalRes(gt,dt,self.exps[i][4])
				res.gtr = gtr
				res.dtr = dtr
				self.res[i].append(res)
		return


	def load_mat_gt(self, gt_setting):
		gtp = os.path.join(gt_path, gt_setting+'.mat')
		print 'handle gt path:', gtp
		assert os.path.exists(gtp)
		gt = sio.loadmat(gtp)
		gt = gt['gt']
		gt = [item for item in gt[0]]
		self.gt[gt_setting] = gt
		assert len(gt) == 4024
		#np.savetxt(gt_setting+'.txt',gt, fmt="%s", newline='\n')
		return
	def bb_resize(self, bb, hr, wr, ar):
		'''
		sresize bbs without moving their centers
		bb [N*4] ori bb
		hr ratio by which to multiply height (or 0)
		wr ratio...weight(or 0)
		ar [0] target aspect ratio (used only if hr=0 or wr=0)
		bb [N*4] output resized bbs
		''' 
		assert (hr>0 and wr>0 or ar>0)
		if(hr==0 and wr==0):
			#a = math.sqrt(bb[:,2]*bb[:,3])
			a = np.array([math.sqrt(scal) for scal in bb[:,2]*bb[:,3]])
			ar = math.sqrt(ar)
			d = a*ar-bb[:,2]
			bb[:,0] = bb[:,0] - d/2
			bb[:,2] = bb[:,2] + d
			d = a/ar - bb[:,3]
			bb[:,1] = bb[:,1] - d/2
			bb[:,3] = bb[:,3] + d
			return bb
		if (hr != 0):
			d = (hr-1)*bb[:,3]
			bb[:,1] = bb[:,1] - d/2
			bb[:,3] = bb[:,3] + d
		if (wr != 0):
			d = (wr-1)*bb[:,2]
			bb[:,0] = bb[:,0] - d/2
			bb[:,2] = bb[:,2] + d
		if(hr == 0):
			d=bb[:,2]/ar-bb[:,3]
			bb[:,1]=bb[:,1]-d/2
			bb[:,3]=bb[:,3]+d
		if(wr==0):
			d=bb[:,3]*ar-bb[:,2]
			bb[:,0]=bb[:,0]-d/2
			bb[:,2]=bb[:,2]+d
		return bb
	
        def read_our_method_dt(self, alg_name):
                alg_path = os.path.join(self.ans_path, alg_name, 'detections.pkl')
                assert os.path.exists(alg_path)
                with open(alg_path,'rb') as f:
                        dt = cPickle.load(f)
                        assert len(dt) == 2
                        dt = dt[1]
                        assert len(dt) == 4024
                        self.ans[alg_name] = dt
                        for i in range(len(dt)):
                                s1 = dt[i][:,0:2]
                                s2 = dt[i][:,2]-dt[i][:,0]
                                s3 = dt[i][:,3]-dt[i][:,1]
                                s4 = dt[i][:,4]
                                s2 = s2.reshape(len(s2),1)
                                s3 = s3.reshape(len(s3),1)
                                s4 = s4.reshape(len(s4),1)
                                dt[i] = np.hstack((s1,s2,s3,s4))
                                #dt[i] = dt[i][np.where(dt[i][:,4]>0.7)[0],:]不加这个反而好了呢
                
	def read_single_dt(self, alg_name):
		alg_path = os.path.join(self.ans_path,alg_name)
		print 'handle alg:', alg_name, 'path:', alg_path
		sets = [f  for f,_,_ in os.walk(alg_path) if 'set' in f]
		assert len(sets)==5
		sets.sort()
		i = 5
		l = []

		for tset in sets:
			i = i+1
			print 'handle:',tset
			for _,_,f in os.walk(tset):
				assert len(f) == len(np.where(self.frame_num_info[:,0]==i)[0])
				#	assert False
				f.sort()
				j = -1
				for files in f:
					j = j+1
					assert files.endswith('txt')
					tmpfr = self.frame_num_info[np.where(self.frame_num_info[:,0] == i)[0],:]
					tmpfr = tmpfr[np.where(tmpfr[:,1]==j)[0],2]
					#tmpfr = np.where(self.frame_num_info[np.where(self.frame_num_info[:,0]==i)[0],1]==j)[0]
					tmpfrs = np.arange(30,tmpfr+1,30)
					self.debug.append(tmpfr)
					self.item.append(len(tmpfrs))
					assert os.path.exists(os.path.join(tset,files))
					dt_ori = np.loadtxt(os.path.join(tset,files))

					for skip in tmpfrs:
						single = dt_ori[np.where(dt_ori[:,0]==skip)[0],1:6]
						l.append(single)
		#np.savetxt(alg_name+'1.txt',l,fmt="%s",newline='\n')
		if self.resize[alg_name] == 1:
			resizev = 100.0/128
		else:
			resizev = 1.0
		for i in range(len(l)):
			l[i] = self.bb_resize(l[i],resizev,0,self.aspectRatio)

		#np.savetxt(alg_name+'.txt',l,fmt="%s",newline='\n')
		self.ans[alg_name]=l
	
	def read_all_dt(self,algs):
		for alg in algs:
                        if alg == 'OurMethod':
                                self.read_our_method_dt(alg)
                                #self.read_single_dt(alg)
                        else:
			        self.read_single_dt(alg)
		
	def compRoc(self, gt, dt, roc, ref):
		#return xs,ys,score(detection score corresponding to each(x,y),ref)
		nImg = len(gt)
		assert nImg == len(dt)
		gt = np.vstack(gt)
		gt = gt[np.where(gt[:,4]!=-1)[0],:]
		dt = np.vstack(dt)
		dt = dt[np.where(dt[:,5]!=-1)[0],:]
		if dt.shape[0] == 0:
			xs = 0
			ys = 0
			score = 0
			ref = ref*0
			return xs,ys,score,ref
		m = ref.shape[0]
		assert len(ref) == ref.shape[0]
		np_ = gt.shape[0]
		score = dt[:,4]
		tp = dt[:,5]
		order = np.argsort(-score)
		score = score[order]
		tp = tp[order]
		fp = (tp!=1).astype(float)
		fp = np.cumsum(fp)
		tp = np.cumsum(tp)
		if roc:
			xs = fp/nImg
			ys = tp/np_
			xs1 = np.hstack((np.array([-inf]),xs))
			ys1 = np.hstack((np.zeros(1),ys))
			for i in range(m):
				j = np.where(xs1<=ref[i])[0]
				ref[i]=ys1[j[-1]]
		else:
			assert False
		return xs,ys,score,ref

	
	def plotExps(self, plotRoc, samples):
		ngt = len(self.res)
		ndt = len(self.res[0])
		#xs = [[] for i in range(ngt)]
		#ys = [[] for i in range(ngt)]
		#scores = np.zeros((ndt,ngt))
		for i in range(ngt):
			for j in range(ndt):
				[xs0,ys0,_,score] = self.compRoc(self.res[i][j].gtr,self.res[i][j].dtr, plotRoc, samples.copy())
				if(plotRoc):
					ys0 = 1-ys0
					score = 1-score
				if(plotRoc):
					score = math.exp(np.mean([math.log(w*1.0) for w in score]))
				else:
					score = np.mean(score)

				#xs[i].append(xs0)
				#ys[i].append(ys0)
				#scores[i,j] = score
				self.res[i][j].xs = xs0
				self.res[i][j].ys = ys0
				self.res[i][j].score = score
				print self.res[i][j].stra,self.res[i][j].stre,score

	def mainp(self):
		algs = self.resize.keys()
		exps = ['gt-Reasonable','gt-All','gt-Scale=near']#需要和self.exp里一一对应
		plotRoc = True
		self.read_all_dt(algs)
		for exp in exps:
			self.load_mat_gt(exp)
		gts = self.gt.values()
		dts = self.ans.values()
		print len(gts),len(dts)
		self.evalAlgs(gts,dts)
		#print self.samples
		self.plotExps(plotRoc, self.samples.copy())
		#print self.samples

a = EVALclatech(nframe_path,ans_path)
a.mainp()
#wxygt = np.array([[  21.25774509,  148.50047592,   59.77196321,  145.78527611,    0.        ],
#       [ 569.02988691,  158.15139898,   22.21434582,   59.08527307,    1.        ],
#       [ 187.5538979 ,  178.55676993,   21.28898392,   51.92435102,    0.        ],
#       [ 224.09167949,  167.40272225,   24.87232111,   60.66419784,    0.        ],
#       [ 259.42096363,  174.83995453,   22.08406956,   53.86358429,    0.        ],
#       [  12.29535529,  192.94830918,   33.95668963,   47.24251208,    1.        ],
#       [ 211.46497412,  168.85309862,   26.36817174,   64.312614  ,    0.        ],
#       [ 159.9601423 ,  173.99765848,   23.73750143,   57.89634495,    0.        ],
#       [  13.24948779,  181.98017929,   21.89008094,   53.84418947,    1.        ],
#       [ 288.37496448,  179.75426257,   28.00929241,   48.92065928,    1.        ]])
#wxydt = np.array([[  19.61225,  153.51   ,   63.7755 ,  155.55   ,  234.25   ],
#       [ 218.36115,  167.24   ,   28.2777 ,   68.97   ,  161.23   ],
#       [ 258.97305,  176.71   ,   22.4639 ,   54.79   ,  158.96   ],
#       [ 289.66305,  178.9    ,   22.4639 ,   54.79   ,  119.97   ],
#       [ 207.33115,  170.     ,   28.2777 ,   68.97   ,   98.47   ],
#       [ 165.3093 ,  171.38   ,   25.2314 ,   61.54   ,   75.2    ],
#       [ 182.89825,  159.87   ,   31.7135 ,   77.35   ,   62.13   ],
#       [ 455.9216 ,   89.78   ,   17.8268 ,   43.48   ,   42.75   ],
#       [ 503.6929 ,   25.71   ,  100.7042 ,  245.62   ,   41.92   ],
#       [ 306.3616 ,  185.43   ,   17.8268 ,   43.48   ,   23.05   ],
#       [ 109.8416 ,  187.17   ,   17.8268 ,   43.48   ,   12.86   ],
#       [  84.0182 ,  123.91   ,   35.6536 ,   86.96   ,    7.53   ]])
#[wxygtr, wxydtr] = a.evalResmini(wxygt,wxydt)
#print wxygtr,wxydtr
#error answer:
#(Pdb) p wxy.gtr[1209]
#array([[  21.25774509,  148.50047592,   59.77196321,  145.78527611,    1.        ],
#       [ 187.5538979 ,  178.55676993,   21.28898392,   51.92435102,   -0.        ],
#       [ 224.09167949,  167.40272225,   24.87232111,   60.66419784,   -0.        ],
#       [ 259.42096363,  174.83995453,   22.08406956,   53.86358429,    1.        ],
#       [ 211.46497412,  168.85309862,   26.36817174,   64.312614  ,    1.        ],
#       [ 159.9601423 ,  173.99765848,   23.73750143,   57.89634495,    1.        ],
#       [ 569.02988691,  158.15139898,   22.21434582,   59.08527307,   -1.        ],
#       [  12.29535529,  192.94830918,   33.95668963,   47.24251208,   -1.        ],
#       [  13.24948779,  181.98017929,   21.89008094,   53.84418947,   -1.        ],
#       [ 288.37496448,  179.75426257,   28.00929241,   48.92065928,   -1.        ]])
#(Pdb) p wxy.dtr[1209]
#array([[  19.61225,  153.51   ,   63.7755 ,  155.55   ,  234.25   ,    1.     ],
#       [ 218.36115,  167.24   ,   28.2777 ,   68.97   ,  161.23   ,    1.     ],
#       [ 258.97305,  176.71   ,   22.4639 ,   54.79   ,  158.96   ,    1.     ],
#       [ 289.66305,  178.9    ,   22.4639 ,   54.79   ,  119.97   ,   -1.     ],
#       [ 207.33115,  170.     ,   28.2777 ,   68.97   ,   98.47   ,    0.     ],
#       [ 165.3093 ,  171.38   ,   25.2314 ,   61.54   ,   75.2    ,    1.     ],
#       [ 182.89825,  159.87   ,   31.7135 ,   77.35   ,   62.13   ,    0.     ],
#       [ 455.9216 ,   89.78   ,   17.8268 ,   43.48   ,   42.75   ,    0.     ],
#       [ 503.6929 ,   25.71   ,  100.7042 ,  245.62   ,   41.92   ,    0.     ],
#       [ 306.3616 ,  185.43   ,   17.8268 ,   43.48   ,   23.05   ,   -1.     ],
#       [ 109.8416 ,  187.17   ,   17.8268 ,   43.48   ,   12.86   ,    0.     ],
#       [  84.0182 ,  123.91   ,   35.6536 ,   86.96   ,    7.53   ,    0.     ]])
#

#		self.argsresize={"CCF":0 "ACF++":0}
