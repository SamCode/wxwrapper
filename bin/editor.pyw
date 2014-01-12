import wx
from wxwrapper import base

class FormDialog(wx.Dialog):
    """A wx.Dialog containing a form."""

    def __init__(self, title):
        super(FormDialog, self).__init__(
            None,
            title = title,
            style = 
                wx.CAPTION |
                wx.SYSTEM_MENU |
                wx.THICK_FRAME)

class NewWindowDialog(FormDialog):
    """...

    Instance variables:
        app
        title_sizer
        title_label
        title_entry
    """

    def __init__(self, app):
        super(NewWindowDialog, self).__init__("New Window")

        self.app = app

        s0 = wx.BoxSizer(wx.VERTICAL)
        self.title_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.title_label = wx.StaticText(self, label = "Title")
        self.title_entry = wx.TextCtrl(self)
        ok = wx.Button(self, wx.ID_ANY, "OK")

        self.title_sizer.AddSpacer((5, 0))
        self.title_sizer.Add(self.title_label, flag = wx.ALIGN_CENTER)
        self.title_sizer.AddSpacer((5, 0))
        self.title_sizer.Add(self.title_entry)
        self.title_sizer.Add(ok)
        s0.Add(self.title_sizer)

        self.SetSizer(s0)

        self.Bind(wx.EVT_BUTTON, self.OnOk, ok)
        self.Fit()

    def prompt(self):
        self.ShowModal()

    def OnOk(self, e):
        title = self.title_entry.GetValue()

        if title not in self.app.windows:
            self.EndModal(self.GetReturnCode())
            self.app.new_window(title)
        else:
            pass
            # display error message

class NewWidgetDialog(FormDialog):
    """...

    Instance variables:
        app
        title_sizer
        title_label
        title_entry
        type_sizer
        type_label
        type_entry
        window
    """

    def __init__(self, app):
        super(NewWidgetDialog, self).__init__("New Widget")

        self.app = app

        s0 = wx.BoxSizer(wx.VERTICAL)

        self.title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.title_label = wx.StaticText(self, label = "Title")
        self.title_entry = wx.TextCtrl(self)

        self.title_sizer.AddSpacer((5, 0))
        self.title_sizer.Add(self.title_label, flag = wx.ALIGN_CENTER)
        self.title_sizer.AddSpacer((5, 0))
        self.title_sizer.Add(self.title_entry)

        self.type_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.type_label = wx.StaticText(self, label = "Type")
        self.type_entry = wx.ComboBox(self)
        self.type_entry.SetItems(sorted(base.WIDGETS.keys()))

        self.type_sizer.AddSpacer((5, 0))
        self.type_sizer.Add(self.type_label, flag = wx.ALIGN_CENTER)
        self.type_sizer.AddSpacer((5, 0))
        self.type_sizer.Add(self.type_entry)

        ok = wx.Button(self, wx.ID_OK, "OK")
        s0.Add(self.title_sizer)
        s0.Add(self.type_sizer)
        s0.Add(ok, flag = wx.ALIGN_RIGHT)

        self.SetSizer(s0)
        self.Bind(wx.EVT_BUTTON, self.OnOk, ok)
        self.Fit()

    def prompt(self, window):
        self.window = window
        self.ShowModal()

    def OnOk(self, e):
        title = self.title_entry.GetValue()
        wtype = self.type_entry.GetValue()

        all_widgets = self.window.all_widgets()

        if (all_widgets is None) or (title not in all_widgets):
            self.EndModal(self.GetReturnCode())

            # Instantiate and install references to a new Widget.
            self.window.widgets[wtype][title] = base.Widget(title)
            self.app.widgets_lb.Insert(title, 0)
        else:
            pass
            # display error message

class Editor(wx.App):
    """The GUI for making GUIs.

    Instance variables:
        windows - a dict in the format:
            key - string; Window identifier
            value - Window instance
        frame - the program's main wx.frame instance
        windows_lb - wx.ListBox
        widgets_lb - wx.ListBox
        windows_display - wx.Button
        windows_edit - wx.Button
        windows_del - wx.Button
        widgets_new - wx.Button
        widgets_edit - wx.Button
        widgets_del - wx.Button
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
        self.init_gui_main()
        self.new_window_dialog = NewWindowDialog(self)
        self.new_widget_dialog = NewWidgetDialog(self)

        self.windows_display.Disable()
        self.windows_edit.Disable()
        self.windows_del.Disable()
        self.widgets_new.Disable()
        self.widgets_edit.Disable()
        self.widgets_del.Disable()

        # show GUI
        self.frame.Fit()
        self.frame.Show()

        # run wxPython
        self.MainLoop()

    def init_menus(self):
        """Set up the editor's menu bar."""

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

    def init_gui_main(self):
        """Set up the editor's main interface."""

        # ListBox of windows

        left_half = wx.BoxSizer(wx.VERTICAL)
        l0 = wx.BoxSizer(wx.HORIZONTAL)

        l1 = wx.BoxSizer(wx.VERTICAL)
        self.windows_lb = wx.ListBox(self.frame)
        l1.Add(self.windows_lb)

        l2 = wx.BoxSizer(wx.VERTICAL)
        windows_new = wx.Button(self.frame, wx.ID_ANY, "New")
        self.windows_display = wx.Button(self.frame, wx.ID_ANY, "Display")
        self.windows_edit = wx.Button(self.frame, wx.ID_ANY, "Edit")
        self.windows_del = wx.Button(self.frame, wx.ID_ANY, "Delete")
        l2.Add(windows_new)
        l2.Add(self.windows_display)
        l2.Add(self.windows_edit)
        l2.Add(self.windows_del)

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
        self.widgets_new = wx.Button(self.frame, wx.ID_ANY, "New")
        self.widgets_edit = wx.Button(self.frame, wx.ID_ANY, "Edit")
        self.widgets_del = wx.Button(self.frame, wx.ID_ANY, "Delete")
        r2.Add(self.widgets_new)
        r2.Add(self.widgets_edit)
        r2.Add(self.widgets_del)

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
        self.frame.Bind(wx.EVT_BUTTON, self.OnDelWindow, self.windows_del)
        self.frame.Bind(wx.EVT_LISTBOX, self.OnSelectWidget, self.widgets_lb)
        self.frame.Bind(wx.EVT_BUTTON, self.OnNewWidget, self.widgets_new)
        self.frame.Bind(wx.EVT_BUTTON, self.OnDelWidget, self.widgets_del)

    def new_window(self, title):
        """Instantiate and install references to a new Window."""

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

    def OnExit(self, e):
        """Exit the editor."""

        self.frame.Close(True)
        exit()

    def OnNewWindow(self, e):
        """Create a dialog prompting the user to initialize a new window."""

        self.new_window_dialog.prompt()

    def OnDelWindow(self, e):
        """Remove references to the Window object represented by the
        selected item in self.windows_lb."""

        i = self.windows_lb.GetSelection()
        if i is not wx.NOT_FOUND:
            title = self.windows_lb.GetString(i)
            del self.windows[title]
            self.windows_lb.Delete(i)

    def OnNewWidget(self, e):
        """Create a dialog prompting the user to create a new widget
        on the selected window."""

        window = self.get_selected_window()
        if window:
            self.new_widget_dialog.prompt(window)

    def OnDelWidget(self, e):
        """Remove references to the Widget object represented by the
        selected item in self.windows_lb."""

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

    def OnSelectWindow(self, e):
        """Update the widgets listbox for the selected window."""

        self.windows_display.Enable()
        self.windows_edit.Enable()
        self.windows_del.Enable()
        self.widgets_new.Enable()

        # Disable certain buttons when a Widget is not selected in the listbox.
        self.widgets_edit.Disable()
        self.widgets_del.Disable()

        window = self.get_selected_window()
        widgets = window.all_widgets()
        if widgets:
            self.widgets_lb.SetItems(window.all_widgets())
        else:
            self.widgets_lb.Clear()

    def OnDeselectWindow(self, e):
        """Disable certain buttons when a Window is not selected
        in the listbox."""

        # Can this event even happen?
        self.windows_display.Disable()
        self.windows_edit.Disable()
        self.windows_del.Disable()

    def OnSelectWidget(self, e):
        """..."""

        self.widgets_edit.Enable()
        self.widgets_del.Enable()
        

if __name__ == "__main__":
    app = Editor()
    app.run()