import wx

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
        self.widgets = {t: [] for t in Editor.WIDGETS.keys()}

    def render(self):
        """Display the wx.Frame containing widgets configured as in 
        self.widgets."""
        self.frame.Fit()
        self.frame.Show()

    def hide(self):
        self.frame.Hide()

class Editor(wx.App):
    """...

    Class variables:
        WIDGETS - a mapping from strings to the widget class objects that
            they represent

    Instance variables:
        windows - a list of Window instances
        frame - the program's main wx.frame instance
        windows_lb - 
    """

    WIDGETS = {
        "Button": wx.Button,
        "Slider": wx.Slider}

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
        self.frame.SetSizer(self.sizer)
        self.frame.SetBackgroundColour(wx.Colour(255, 255, 255))

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
        self.windows_lb = wx.ListBox(self.frame)
        l1.Add(self.windows_lb)

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

        self.frame.Bind(wx.EVT_BUTTON, self.OnNewWindow, windows_new)

    def OnExit(self, e):
        """Exit the editor."""

        self.frame.Close(True)

    def OnNewWindow(self, e):
        """..."""

        dialog = wx.Dialog(
            None,
            title = "New Window",
            style = 
                wx.DEFAULT_DIALOG_STYLE | 
                wx.THICK_FRAME)

        s0 = wx.BoxSizer(wx.VERTICAL)
        s1 = wx.BoxSizer(wx.HORIZONTAL)

        title_label = wx.StaticText(dialog, label = "Title")
        title_entry = wx.TextCtrl(dialog)
        ok = wx.Button(dialog, wx.ID_ANY, "OK")

        s1.Add(title_entry)
        s1.Add(ok)
        s0.Add(title_label)
        s0.Add(s1)

        dialog.Bind(
            wx.EVT_BUTTON, 
            lambda e: dialog.EndModal(dialog.GetReturnCode()), 
            ok)
        dialog.SetSizer(s0)
        dialog.Fit()
        dialog.ShowModal()
        
        # occurs after dialog.EndModal() is called
        dialog.Destroy()

        window = Window(title = title_entry.GetValue())
        self.windows.append(window)
        self.windows_lb.Insert(window.title, 0)

if __name__ == "__main__":
    app = Editor()
    app.run()