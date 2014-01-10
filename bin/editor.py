import wx
from wxwrapper import base

class FormDialog(wx.Dialog):
    """A wx.Dialog containing a form."""

    def __init__(self, title):
        wx.Dialog.__init__(self,
            None,
            title = title,
            style = 
                wx.CAPTION |
                wx.SYSTEM_MENU |
                wx.THICK_FRAME)

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
        self.widgets_lb = wx.ListBox(self.frame)
        r1.Add(self.widgets_lb)

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
        self.frame.Bind(wx.EVT_BUTTON, self.OnNewWidget, widgets_new)
        self.frame.Bind(wx.EVT_BUTTON, self.OnDelWidget, widgets_del)

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
            self.windows_lb.Delete(i)
            title = self.windows_lb.GetString(i)
            del self.windows[title]

    def OnExit(self, e):
        """Exit the editor."""

        self.frame.Close(True)
        exit()

    def OnNewWindow(self, e):
        """Create a dialog prompting the user to initialize a new window."""

        dialog = FormDialog("New Window")

        s0 = wx.BoxSizer(wx.VERTICAL)
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)

        title_label = wx.StaticText(dialog, label = "Title")
        title_entry = wx.TextCtrl(dialog)
        ok = wx.Button(dialog, wx.ID_ANY, "OK")

        title_sizer.AddSpacer((5, 0))
        title_sizer.Add(title_label, flag = wx.ALIGN_CENTER)
        title_sizer.AddSpacer((5, 0))
        title_sizer.Add(title_entry)
        title_sizer.Add(ok)
        s0.Add(title_sizer)

        dialog.SetSizer(s0)

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
        
        dialog.Fit()
        dialog.ShowModal()

    def OnDelWindow(self, e):
        """..."""

        self.del_selected_window()

    def OnNewWidget(self, e):
        """Create a dialog prompting the user to create a new widget
        on the selected window."""

        window = self.get_selected_window()
        if not window:
            return

        dialog = FormDialog("New Widget")

        s0 = wx.BoxSizer(wx.VERTICAL)

        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title_label = wx.StaticText(dialog, label = "Title")
        title_entry = wx.TextCtrl(dialog)

        title_sizer.AddSpacer((5, 0))
        title_sizer.Add(title_label, flag = wx.ALIGN_CENTER)
        title_sizer.AddSpacer((5, 0))
        title_sizer.Add(title_entry)

        type_sizer = wx.BoxSizer(wx.HORIZONTAL)
        type_label = wx.StaticText(dialog, label = "Type")
        type_entry = wx.ComboBox(dialog)
        type_entry.SetItems(base.WIDGETS.keys())

        type_sizer.AddSpacer((5, 0))
        type_sizer.Add(type_label, flag = wx.ALIGN_CENTER)
        type_sizer.AddSpacer((5, 0))
        type_sizer.Add(type_entry)

        ok = wx.Button(dialog, wx.ID_ANY, "OK")
        s0.Add(title_sizer)
        s0.Add(type_sizer)
        s0.Add(ok, flag = wx.ALIGN_RIGHT)

        dialog.SetSizer(s0)

        def OnNewWindowOk(e):
            title = title_entry.GetValue()
            wtype = type_entry.GetValue()
            all_widgets = window.all_widgets()
            if (all_widgets is None) or (title not in all_widgets):
                dialog.EndModal(dialog.GetReturnCode())
                dialog.Destroy()
                window.widgets[wtype][title] = base.Widget(title)
                self.widgets_lb.Insert(title, 0)
            else:
                dialog.ShowModal()
                # display error message

        dialog.Bind(wx.EVT_BUTTON, OnNewWindowOk, ok)
        
        dialog.Fit()
        dialog.ShowModal()

        # request widget type
        # listbox.InsertItems(sorted(base.WIDGETS.keys()), 0)
        # request widget title (default is <widget_type><number>)

    def OnSelectWindow(self, e):
        """Update the widgets listbox for the selected window."""

        window = self.get_selected_window()
        widgets = window.all_widgets()
        if widgets:
            self.widgets_lb.SetItems(window.all_widgets())
        else:
            self.widgets_lb.Clear()

    def OnDelWidget(self, e):
        """..."""

        window = self.get_selected_window()
        widget_i = self.widgets_lb.GetSelection()
        widget = self.widgets_lb.GetString(widget_i)
        if widget is not wx.NOT_FOUND:
            for wtype, widgets in window.widgets.iteritems():
                for wtitle in widgets:
                    if wtitle == widget:
                        del window.widgets[wtype][wtitle]
                        self.widgets_lb.Delete(widget_i)
                        break

if __name__ == "__main__":
    app = Editor()
    app.run()