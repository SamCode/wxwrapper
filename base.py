"""...

Global variables:
    WIDGETS - a mapping from strings to the wx.Window class objects that
        they represent
"""

import wx

WIDGETS = {
    "Button": wx.Button,
    "Slider": wx.Slider}

class App(object):
	"""..."""

class Widget(object):
    """Represents a wx.Window."""

    def __init__(self, title):
        self.title = title

class Window(object):
    """A wrapper over a wx.Frame.

    Instance variables:
        frame - the wx.Frame that this Window represents
        widgets - a dict in the format:
            key - string representing the type of widget
            value - a list of dicts representing widgets of that type that are
                    contained in this wx.Frame in the format:
                key - string representing a widget attribute
                value - value of the attribute
    """

    def __init__(self, title, parent=None):
        self.title = title
        self.frame = wx.Frame(
            parent, 
            title = title,
            style = 
                wx.SYSTEM_MENU |
                # wx.RESIZE_BORDER |
                # wx.MINIMIZE_BOX |
                # wx.MAXIMIZE_BOX |
                wx.CLOSE_BOX |
                wx.CAPTION | 
                wx.CLIP_CHILDREN)
        self.widgets = {t: [] for t in WIDGETS.keys()}

    def render(self):
        """Display the wx.Frame containing widgets configured as in 
        self.widgets."""

        # Render each of the widgets.
        # Show Frame.
        self.frame.Fit()
        self.frame.Show()

    def hide(self):
        self.frame.Hide()