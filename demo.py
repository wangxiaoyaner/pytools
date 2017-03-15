import wx
import noname as demo
class CalcFrame(demo.MyFrame1):
    def __init(self, parent):
        demo.MyFrame1.__init__(self, parent)
    def findsquare(self, event):
        num = int(self.m_textCtrl2.GetValue())
        self.m_textCtrl3.SetValue(str(num*num))

app = wx.App(False)
frame = CalcFrame(None)
frame.Show(True)
app.MainLoop()
