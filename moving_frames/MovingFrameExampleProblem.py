import wx

"""
Demonstrates the problem with MovingFrame which neccesitated a steady
window in the form of FocusFrame.
Clicking on another window causes the current app to lose focus.  Catching this
allows it to be returned, as done in the final clause of FilterEvent.
However the focus can only be successfully returned once, subsequently it is
not returned successfully.  

"""
class MovingFrameExampleProblem(wx.Frame):
    
    def __init__(self, speed=20):

        self.speed = speed
        wx.Frame.__init__(self, None, 1, "title", pos=(0,0),
                  size=(100,100), style=
                  wx.NO_BORDER| wx.FRAME_NO_TASKBAR |wx.STAY_ON_TOP)
          
        self.panel = wx.Panel(self, size=self.GetSize())
        self.SetBackgroundColour((200,0,0))
        self.panel.SetFocus()
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.Move, self.timer)
        self.timer.Start(self.speed)

    def Move(self, event):
        pos = self.GetPosition()
        (width, height) = wx.DisplaySize()
        (x, y) = self.GetSize()
        if pos.x + x < width:
            pos.x += 2
            self.SetPosition(pos)
        self.Refresh()

    def ToggleStopStart(self, event):
        if self.timer.IsRunning():
            self.timer.Stop()
        else:
            self.timer.Start(self.speed)

    def CloseWindow(self, event):
        self.Close()  
        self.Show(False)
        event.Skip()


if __name__ == "__main__": 
    class MyApp(wx.App):
        def OnInit(self):
            self.frame = MovingFrameExampleProblem()  
            self.frame.Show(True)
            return True

        def FilterEvent(self, event):
            if event.GetEventType() == wx.wxEVT_KEY_DOWN:
                key = event.GetKeyCode()
                if key == wx.WXK_ESCAPE:
                    self.frame.CloseWindow(event)
                    self.ExitMainLoop() 
                    return True
                elif key == wx.WXK_SPACE:
                    self.frame.ToggleStopStart(event)
            elif event.GetEventType() == wx.wxEVT_KILL_FOCUS:
                print 'The window ID:', event.GetEventObject().GetId(),
                print ' is losing focus'
                wx.FutureCall(1000,self.frame.panel.SetFocus)
            return -1

            
  
    app = MyApp(0)
    app.SetCallFilterEvent(True)
    app.MainLoop()
