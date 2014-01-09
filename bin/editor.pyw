import wx
from wxwrapper import base

class Editor(wx.App):
    """...

    Class variables:
        WIDGETS - a mapping from strings to the widget class objects that
            they represent

    Instance variables:
        windows - a list of base.Window instances
        frame - the program's main wx.frame instance
    """

    WIDGETS = {
        "Button": wx.Button,
        "Slider": wx.Slider,
    }

    def __init__(self):
        wx.App.__init__(self)

        self.windows = []
        self.active_window = None

    def run(self):
        """Run the editor."""

        # init Frame
        self.frame = wx.Frame(
            None, 
            title = "wxEditor", 
            # size = (400, 400),
            style = 
                wx.SYSTEM_MENU |
                # wx.RESIZE_BORDER |
                # wx.MINIMIZE_BOX |
                # wx.MAXIMIZE_BOX |
                wx.CLOSE_BOX |
                wx.CAPTION | 
                wx.CLIP_CHILDREN)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        container = wx.BoxSizer(wx.HORIZONTAL)
        container.AddSpacer((0, 0), 1, wx.EXPAND)
        container.Add(self.sizer, 0, wx.EXPAND | wx.ALL, 5)
        container.AddSpacer((0, 0), 1, wx.EXPAND)
        self.frame.SetSizer(container)

        # init rest of GUI
        self.init_menus()
        self.init_edit_main()
        # self.init_edit_1()
        # self.init_edit_2()

        # show GUI
        self.frame.Fit()
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

        # ListBox of windows

        left_half = wx.BoxSizer(wx.VERTICAL)
        l0 = wx.BoxSizer(wx.HORIZONTAL)

        l1 = wx.BoxSizer(wx.VERTICAL)
        windows = wx.ListBox(self.frame)
        l1.Add(windows)

        l2 = wx.BoxSizer(wx.VERTICAL)
        windows_new = wx.Button(self.frame, wx.ID_ANY, "New")
        windows_display = wx.Button(self.frame, wx.ID_ANY, "Display")
        windows_edit = wx.Button(self.frame, wx.ID_ANY, "Edit")
        windows_del = wx.Button(self.frame, wx.ID_ANY, "Delete")
        l2.Add(windows_new)
        l2.Add(windows_display)
        l2.Add(windows_edit)
        l2.Add(windows_del)

        l0.Add(l1)
        l0.Add(l2)

        windows_label = wx.StaticText(self.frame, label = "Windows")
        left_half.Add(windows_label)
        left_half.Add(l0)

        # new (Widget) button > dialog with ListBox of widget types

        right_half = wx.BoxSizer(wx.VERTICAL)
        r0 = wx.BoxSizer(wx.HORIZONTAL)

        r1 = wx.BoxSizer(wx.VERTICAL)
        widgets = wx.ListBox(self.frame)
        r1.Add(widgets)

        r2 = wx.BoxSizer(wx.VERTICAL)
        widgets_new = wx.Button(self.frame, wx.ID_ANY, "New")
        widgets_edit = wx.Button(self.frame, wx.ID_ANY, "Edit")
        widgets_del = wx.Button(self.frame, wx.ID_ANY, "Delete")
        r2.Add(widgets_new)
        r2.Add(widgets_edit)
        r2.Add(widgets_del)
        # listbox.InsertItems(sorted(Editor.WIDGETS.keys()), 0)

        r0.Add(r1)
        r0.Add(r2)

        widgets_label = wx.StaticText(self.frame, label = "Widgets")
        right_half.Add(widgets_label)
        right_half.Add(r0)

        # arrange sizers on frame
        self.sizer.Add(left_half)
        self.sizer.AddSpacer((10, 0))
        self.sizer.Add(right_half)

    def OnExit(self, e):
        self.frame.Close(True)

if __name__ == "__main__":
    app = Editor()
    app.run()