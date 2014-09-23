import wx
import time

"""
A simple frame which moves across the screen until stopped either top to
bottom or left to right.
Used to specify a particular piece of the screen
"""

#to use later if window is losing focus
# self.ToggleWindowStyle(wx.STAY_ON_TOP)
"""
to do:
- add custom events (or functions), callable by the main overseer:
    - one of them to close the frame
    - another one to stop it and return its current position
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

        self.panel.Bind(wx.EVT_RIGHT_UP, self.CloseWindow)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
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

    def OnKeyDown(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_ESCAPE:
            self.CloseWindow(event)
        event.Skip()
        

    def CloseWindow(self, event):
        self.Close()
        self.Show(False)
        event.Skip()


if __name__ == "__main__":
    class MyApp(wx.App):
        def OnInit(self):
            frame = MovingFrame()
            frame.Show(True)
            frame2 = MovingFrame(moving_horizontally=False)
            frame2.Show(True)
            self.SetTopWindow(frame)
            return True
    app = MyApp(0)
    app.MainLoop()
