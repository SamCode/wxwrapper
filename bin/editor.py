import wx
from wxwrapper import base

class Editor(wx.App):
    """...

    Instance variables:
        windows - a dict in the format:
            key - string; Window identifier
            value - Window instance
        frame - the program's main wx.frame instance
        windows_lb - 
    """

    def __init__(self):
        wx.App.__init__(self)

        self.windows = {}
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

        r0.Add(r1)
        r0.Add(r2)

        widgets_label = wx.StaticText(self.frame, label = "Widgets")
        right_half.Add(widgets_label)
        right_half.Add(r0)

        # arrange sizers on frame
        self.sizer.Add(left_half)
        self.sizer.AddSpacer((10, 0))
        self.sizer.Add(right_half)

        # bind events
        self.frame.Bind(wx.EVT_LISTBOX, self.OnSelectWindow, self.windows_lb)
        self.frame.Bind(wx.EVT_BUTTON, self.OnNewWindow, windows_new)
        self.frame.Bind(wx.EVT_BUTTON, self.OnDelWindow, windows_del)

    def new_window(self, title):
        """..."""

        assert title not in self.windows
        window = base.Window(title = title)
        self.windows[title] = window
        self.windows_lb.Insert(window.title, 0)

    def get_selected_window(self):
        """Returns the Window object represented by the selected item
        in self.windows_lb."""

        i = self.windows_lb.GetSelection()
        if i is not wx.NOT_FOUND:
            title = self.windows_lb.GetString(i)
            return self.windows[title]

    def del_selected_window(self):
        """Remove references to the Window object represented by the
        selected item in self.windows_lb."""

        i = self.windows_lb.GetSelection()
        if i is not wx.NOT_FOUND:
            title = self.windows_lb.GetString(i)
            del self.windows[title]

    def OnExit(self, e):
        """Exit the editor."""

        self.frame.Close(True)
        exit()

    def OnNewWindow(self, e):
        """Create a dialog prompting the user to initialize a new window."""

        dialog = wx.Dialog(
            None,
            title = "New Window",
            style = 
                wx.CAPTION |
                wx.SYSTEM_MENU |
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

        def OnNewWindowOk(e):
            title = title_entry.GetValue()
            if title not in self.windows:
                dialog.EndModal(dialog.GetReturnCode())
                dialog.Destroy()
                self.new_window(title)
            else:
                dialog.ShowModal()
                # display error message

        dialog.Bind(wx.EVT_BUTTON, OnNewWindowOk, ok)
        dialog.SetSizer(s0)
        dialog.Fit()
        dialog.ShowModal()

    def OnDelWindow(self, e):
        """..."""

        self.del_selected_window()

    def OnNewWidget(self, e):
        """Create a dialog prompting the user to create a new widget
        on the selected window."""

        # request widget type
        # listbox.InsertItems(sorted(base.WIDGETS.keys()), 0)
        # request widget title (default is <widget_type><number>)

    def OnSelectWindow(self, e):
        """Update the widgets listbox for the selected window."""

        window = self.get_selected_window()
        self.widgets.lb.InsertItems(window.widgets.itervalues())

if __name__ == "__main__":
    app = Editor()
    app.run()