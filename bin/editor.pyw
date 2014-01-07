import wx

class Editor(wx.App):
    """...

    Instance variables:
        frame - the program's main wx.frame instance
        widgets - a dict in the format:
            {
                <window>: {
                    <widget type>: [
                        {
                            <widget attribute>: <value>, 
                            ...
                        }, 
                        ...
                    ],
                ...
            }
    """

    WIDGETS = {
        "Button": wx.Button,
        "Slider": wx.Slider,
    }

    def __init__(self):
        wx.App.__init__(self)

        self.widgets = {}

        # new window frame

        # edit window frame
        self.active_window = None

    def run(self):
        """Run the program."""

        self.init_gui()
        self.MainLoop()

    def init_gui(self):
        """Set up editor GUI."""

        # File menu
        file_menu = wx.Menu()
        load_item = file_menu.Append(wx.ID_ANY, "&Load", 
            "Open work previously saved using this program.")
        save_item = file_menu.Append(wx.ID_ANY, "&Save", 
            "Store your progress on your computer.")
        file_menu.AppendSeparator()
        exit_item = file_menu.Append(wx.ID_EXIT, "E&xit", "Terminate the program.")

        # Init MenuBar instance.
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")

        # Init wx.Frame instance.
        self.frame = wx.Frame(None, title = "wxEditor", size = (400, 400))
        self.frame.SetMenuBar(menu_bar)
        self.frame.CreateStatusBar()

        # Bind events.
        self.frame.Bind(wx.EVT_MENU, self.OnExit, exit_item)

        # Show the app's GUI.
        self.frame.Show()

    def OnExit(self, e):
        self.frame.Close(True)

if __name__ == "__main__":
    app = Editor()
    app.run()