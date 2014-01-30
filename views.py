"""...

Global variables:
    WIDGETS - a mapping from strings to the wx.Window class objects that
        they represent
"""

import wx

WIDGETS = {
    "Button": wx.Button,
    "Slider": wx.Slider,
    "Listbox": wx.ListBox
}

class Widget(object):
    """Represents a wx.Window.

    Instance variables:
        attrs - 
    """

    def __init__(self, title):
        self.title = title
        self.attrs = {}

class Window(object):
    """Represents a wx.Frame.

    Instance variables:
        title - title of the window
        frame - the wx.Frame that this Window represents
        widgets - a dict in the format:
            key - string representing the type of widget
            value - a dict containing widgets of that type, in the format:
                key - title of a widget
                value - the Widget instance object
    """

    def __init__(self, title, parent=None):
        self.title = title
        self.widgets = {t: {} for t in WIDGETS.keys()}
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

    def all_widgets(self, objects=False):
        """..."""

        def f(x, y):
            z = x.copy()
            z.update(y)
            return z
        if objects:
            return reduce(f, self.widgets.itervalues())
        else:
            return reduce(f, self.widgets.itervalues()).keys()

    def render(self):
        """Display the wx.Frame containing widgets configured as in 
        self.widgets."""

        # Render each of the widgets.
        # Show Frame.
        self.frame.Fit()
        self.frame.Show()

    def hide(self):
        self.frame.Hide()

class FormDialog(wx.Dialog):
    """A wx.Dialog containing a form.

    Instance variables:
        fields - a dict in the format:
            key - name of the form field
            value - a dict with the keys "sizer", "label", and "entry"
                mapped to their corresponding wx objects.
    """

    def __init__(self, title):
        super(FormDialog, self).__init__(
            None,
            title = title,
            style = 
                wx.CAPTION |
                wx.SYSTEM_MENU |
                wx.THICK_FRAME)

        self.fields = {}
        self.sizer = wx.BoxSizer(wx.VERTICAL)

    def init(self):
        """..."""

        self.ok = wx.Button(self, wx.ID_OK, "OK")
        self.sizer.Add(self.ok, flag = wx.ALIGN_RIGHT)

        self.SetSizer(self.sizer)
        self.Fit()

    def add_field(self, name, entry):
        """Initialize a new field."""

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, label = name)

        sizer.AddSpacer((5, 0))
        sizer.Add(label, flag = wx.ALIGN_CENTER)
        sizer.AddSpacer((5, 0))
        sizer.Add(entry)

        self.fields[name] = {
            "sizer": sizer,
            "label": label,
            "entry": entry}

        self.sizer.Add(sizer)

    def add_text_field(self, name):
        """Initialize a new text entry."""

        entry = wx.TextCtrl(self)
        self.add_field(name, entry)

    def add_menu_field(self, name, options):
        """..."""

        entry = wx.ComboBox(self)
        entry.SetItems(options)
        self.add_field(name, entry)

class NewWindowDialog(FormDialog):
    """..."""

    def __init__(self):
        super(NewWindowDialog, self).__init__("New Window")

        self.add_text_field("Title")
        self.init()

    def prompt(self):
        self.ShowModal()

class NewWidgetDialog(FormDialog):
    """...

    Instance variables:
        window
    """

    def __init__(self):
        super(NewWidgetDialog, self).__init__("New Widget")

        self.add_text_field("Title")
        self.add_menu_field("Type", sorted(WIDGETS.keys()))
        self.init()

    def prompt(self, window):
        self.window = window
        self.ShowModal()

class MainFrame(wx.Frame):
    """...

    Instance variables:
        windows - a dict in the format:
            key - string; Window identifier
            value - Window instance
        app - wx.App
        sizer - wx.BoxSizer
        nwind - FormDialog
        nwidd - FormDialog
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
        """Initialize non-wx data structures."""

        self.windows = {}

    def run(self):
        """Run wxPython's event loop."""

        self.wx_init()
        self.app.MainLoop()

    def new_window(self, title):
        """Instantiate and install references to a new Window."""

        assert title not in self.windows
        window = Window(title = title)
        self.windows[title] = window
        self.windows_lb.Insert(window.title, 0)

    def get_selected_window(self):
        """Returns the Window object represented by the selected item
        in self.windows_lb."""

        i = self.windows_lb.GetSelection()
        if i is not wx.NOT_FOUND:
            title = self.windows_lb.GetString(i)
            return self.windows[title]

    def wx_init(self):
        """Initialize wx component."""

        self.app = wx.App()

        super(MainFrame, self).__init__(
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
        self.SetSizer(self.sizer)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        # init rest of GUI
        self.init_menus()
        self.init_gui_main()

        self.nwind = NewWindowDialog()
        self.nwidd = NewWidgetDialog()
        self.nwind.Bind(
            wx.EVT_BUTTON, self.OnNewWindowOk, self.nwind.ok)
        self.nwidd.Bind(
            wx.EVT_BUTTON, self.OnNewWidgetOk, self.nwidd.ok)

        self.windows_display.Disable()
        self.windows_edit.Disable()
        self.windows_del.Disable()
        self.widgets_new.Disable()
        self.widgets_edit.Disable()
        self.widgets_del.Disable()

        # show GUI
        self.Fit()
        self.Show()

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
        self.SetMenuBar(menu_bar)
        self.CreateStatusBar()

        # bind events
        self.Bind(wx.EVT_MENU, self.OnExit, exit_item)

    def init_gui_main(self):
        """Set up the editor's main interface."""

        # ListBox of windows

        left_half = wx.BoxSizer(wx.VERTICAL)
        l0 = wx.BoxSizer(wx.HORIZONTAL)

        l1 = wx.BoxSizer(wx.VERTICAL)
        self.windows_lb = wx.ListBox(self)
        l1.Add(self.windows_lb)

        l2 = wx.BoxSizer(wx.VERTICAL)
        windows_new = wx.Button(self, wx.ID_ANY, "New")
        self.windows_display = wx.Button(self, wx.ID_ANY, "Display")
        self.windows_edit = wx.Button(self, wx.ID_ANY, "Edit")
        self.windows_del = wx.Button(self, wx.ID_ANY, "Delete")
        l2.Add(windows_new)
        l2.Add(self.windows_display)
        l2.Add(self.windows_edit)
        l2.Add(self.windows_del)

        l0.Add(l1)
        l0.Add(l2)

        windows_label = wx.StaticText(self, label = "Windows")
        left_half.Add(windows_label)
        left_half.Add(l0)

        # new (Widget) button > dialog with ListBox of widget types

        right_half = wx.BoxSizer(wx.VERTICAL)
        r0 = wx.BoxSizer(wx.HORIZONTAL)

        r1 = wx.BoxSizer(wx.VERTICAL)
        self.widgets_lb = wx.ListBox(self)
        r1.Add(self.widgets_lb)

        r2 = wx.BoxSizer(wx.VERTICAL)
        self.widgets_new = wx.Button(self, wx.ID_ANY, "New")
        self.widgets_edit = wx.Button(self, wx.ID_ANY, "Edit")
        self.widgets_del = wx.Button(self, wx.ID_ANY, "Delete")
        r2.Add(self.widgets_new)
        r2.Add(self.widgets_edit)
        r2.Add(self.widgets_del)

        r0.Add(r1)
        r0.Add(r2)

        widgets_label = wx.StaticText(self, label = "Widgets")
        right_half.Add(widgets_label)
        right_half.Add(r0)

        # arrange sizers on frame
        self.sizer.Add(left_half)
        self.sizer.AddSpacer((10, 0))
        self.sizer.Add(right_half)

        # bind events
        self.Bind(wx.EVT_LISTBOX, self.OnSelectWindow, self.windows_lb)
        self.Bind(wx.EVT_BUTTON, self.OnNewWindow, windows_new)
        self.Bind(wx.EVT_BUTTON, self.OnDelWindow, self.windows_del)
        self.Bind(wx.EVT_LISTBOX, self.OnSelectWidget, self.widgets_lb)
        self.Bind(wx.EVT_BUTTON, self.OnNewWidget, self.widgets_new)
        self.Bind(wx.EVT_BUTTON, self.OnDelWidget, self.widgets_del)

    def OnExit(self, e):
        """Exit the editor."""

        self.Close(True)
        exit()

    def OnNewWindow(self, e):
        """Create a dialog prompting the user to initialize a new window."""

        self.nwind.prompt()

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
            self.nwidd.prompt(window)

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

    def OnNewWindowOk(self, e):

        title = self.nwind.fields["Title"]["entry"].GetValue()

        if title not in self.windows:
            self.nwind.EndModal(self.nwind.GetReturnCode())
            self.new_window(title)
        else:
            pass
            # display error message

    def OnNewWidgetOk(self, e):

        title = self.nwidd.fields["Title"]["entry"].GetValue()
        wtype = self.nwidd.fields["Type"]["entry"].GetValue()

        all_widgets = self.nwidd.window.all_widgets()

        if (all_widgets is None) or (title not in all_widgets):
            self.nwidd.EndModal(self.nwidd.GetReturnCode())

            # Instantiate and install references to a new Widget.
            self.nwidd.window.widgets[wtype][title] = Widget(title)
            self.widgets_lb.Insert(title, 0)
        else:
            pass
            # display error message