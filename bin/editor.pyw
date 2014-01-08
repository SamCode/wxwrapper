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
        self.active_window = None

    def run(self):
        """Run the editor."""

        # init Frame
        self.frame = wx.Frame(None, title = "wxEditor", size = (400, 400))
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.frame.SetSizer(self.sizer)

        # init rest of GUI
        self.init_menus()
        self.init_edit_main()
        # self.init_edit_1()
        # self.init_edit_2()

        # show GUI
        self.frame.Show()

        # run wxPython
        self.MainLoop()

    def init_menus(self):
        """Set up editor's menu bar."""

        # File menu
        file_menu = wx.Menu()
        load_item = file_menu.Append(
            wx.ID_ANY,
            "&Load", 
            "Open work previously saved using this program.")
        save_item = file_menu.Append(
            wx.ID_ANY,
            "&Save", 
            "Store your progress on your computer.")
        file_menu.AppendSeparator()
        exit_item = file_menu.Append(
            wx.ID_EXIT, 
            "E&xit", 
            "Terminate the program.")

        # init MenuBar instance
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")

        # init wx.Frame instance
        self.frame.SetMenuBar(menu_bar)
        self.frame.CreateStatusBar()

        # bind events
        self.frame.Bind(wx.EVT_MENU, self.OnExit, exit_item)

    def init_edit_main(self):
        """..."""

        left_half = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(left_half)

        # ListBox of windows
        windows = wx.ListBox(self.frame)
        left_half.Add(windows)

        right_half = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(right_half)

        # new (Widget) button > dialog with ListBox of widget types
        widgets = wx.ListBox(self.frame)
        right_half.Add(widgets)
        # listbox.InsertItems(sorted(Editor.WIDGETS.keys()), 0)

    def OnExit(self, e):
        self.frame.Close(True)

if __name__ == "__main__":
    app = Editor()
    app.run()