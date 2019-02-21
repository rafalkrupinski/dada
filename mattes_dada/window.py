# First things, first. Import the wxPython package.
import wx
from .ui.FileDropTarget import FileDropTarget

# Next, create an application object.
app = wx.App()

# Then a frame.
frm = wx.Frame(None, title="Hello World")

drop = FileDropTarget(frm)
frm.SetDropTarget(drop)

# Show it.
frm.Show()

# Start the event loop.
app.MainLoop()
