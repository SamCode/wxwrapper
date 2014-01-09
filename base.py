class App(object):
	"""..."""

class Window(object):
    """A wrapper over a wx.Frame.

    Instance variables:
        frame - the wx.Frame that this Window represents
        widgets - a dict in the format:
            key - string representing the type of widget
            value - a list, representing widgets of that type that are
                	contained in this wx.Frame, of dicts in the format:
            	key - string representing a widget attribute
            	value - value of the attribute
    """

    def __init__(self, parent):
        self.frame = wx.Frame(parent)
        self.widgets = {t: [] for t in Editor.WIDGETS.keys()}

    def render(self):
    	"""Display the wx.Frame containing widgets configured as in 
    	self.widgets."""