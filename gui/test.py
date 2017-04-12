import wx
import noname as demo
class CalcFrame(demo.MyFrame1):
	def __init(self, parent):
        	demo.MyFrame1.__init__(self, parent)
		self.image_path = '/'
	def filePickerOnFileChanged(self, event):
		self.image_path = self.filePicker.GetPath()
		img = wx.Image(self.image_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		self.imageBitMap.SetBitmap(img)
	
app = wx.App(False)
frame = CalcFrame(None)
frame.Show(True)
app.MainLoop()
