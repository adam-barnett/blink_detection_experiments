import wx
import time
from FocusFrame import FocusFrame

"""
A simple frame which moves across the screen until stopped either top to
bottom or left to right.
Used to specify a particular piece of the screen
"""

class MovingFrame(wx.Frame):
    
    def __init__(self, moving_horizontally=True, speed=20):

        self.speed = speed
        (width, height) = wx.DisplaySize()
        if(moving_horizontally):
            width = 6
            self.move = (2,0)
        else:
            height = 6
            self.move = (0,2)
        wx.Frame.__init__(self, None, 1, "title", pos=(0,0),
                  size=(width, height), style=
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
        if pos.x + x < width or pos.y + y < height:
            pos.x += self.move[0]
            pos.y += self.move[1]
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

    def IsMoving(self):
        return self.timer.IsRunning()

    def GivePosition(self):
        pos = self.GetPosition()
        if moving_horizontally:
            return pos.x
        else:
            return pos.y


if __name__ == "__main__":
    class MyApp(wx.App):
        def OnInit(self):
            self.frame1 = MovingFrame()  
            self.frame1.Show(True)
            self.frame2 = MovingFrame(moving_horizontally=False)
            self.frame2.Show(True)
            self.frame3 = FocusFrame()
            self.frame3.Show(True)
            self.SetTopWindow(self.frame1)
            self.Bind(wx.EVT_CHAR_HOOK, self.KeyPress)
            return True

        def KeyPress(self, event):
            if event.GetKeyCode() == wx.WXK_SPACE:
                self.frame1.ToggleStopStart(event)
                self.frame2.ToggleStopStart(event)
            elif event.GetKeyCode() == wx.WXK_ESCAPE:
                self.frame1.CloseWindow(event)
                self.frame2.CloseWindow(event)
                self.frame3.CloseWindow(event)
                self.ExitMainLoop() 
            
    app = MyApp(0)
    app.SetCallFilterEvent(True)
    app.MainLoop()
