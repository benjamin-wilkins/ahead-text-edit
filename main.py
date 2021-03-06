import gi
gi.require_version("Gtk", "3.0")
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Vte, GLib
import os

class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Ahead")
        self.connect("destroy", Gtk.main_quit)
        self.set_size_request(600, 400)
        self.set_icon_name("accessories-text-editor")
        
        self.titlebar = Gtk.HeaderBar()
        self.titlebar.set_show_close_button(True)
        self.titlebar.props.title = "Ahead"
        
        self.toolbarBox = Gtk.HBox()
        Gtk.StyleContext.add_class(self.toolbarBox.get_style_context(), "linked")
        
        self.open = Gtk.Button(label="Open")
        self.open.connect("clicked", self.openTab)
        self.toolbarBox.add(self.open)
        
        self.save = Gtk.Button(label="Save")
        self.save.connect("clicked", self.saveTab)
        self.toolbarBox.add(self.save)
        
        self.saveas = Gtk.Button(label="Save As")
        self.saveas.connect("clicked", self.saveasTab)
        self.toolbarBox.add(self.saveas)
        
        self.new = Gtk.Button(label="New")
        self.new.connect("clicked", self.newTab)
        self.toolbarBox.add(self.new)
        
        self.titlebar.add(self.toolbarBox)
        
        self.set_titlebar(self.titlebar)
        
        self.left_panel = Gtk.Notebook()
        self.left_panel.set_tab_pos(Gtk.PositionType.LEFT)
        self.add(self.left_panel)
        self.edit = Gtk.VBox()
        
        self.tabs = Gtk.Notebook(expand=True)
        self.tabs.set_scrollable(True)
        self.edit.add(self.tabs)
        
        tab = Tab("", self.tabs)
        self.tabs.append_page(tab, tab.label)
        
        self.left_panel.append_page(self.edit, Gtk.Label(label="Edit"))
        
        self.show_all()
    
    def newTab(self, widget):
        tab = Tab("", self.tabs)
        self.tabs.append_page(tab, tab.label)
        self.show_all()
    
    def openTab(self, widget):
        dialogue = Gtk.FileChooserDialog(title="Open", parent=self, action=Gtk.FileChooserAction.OPEN)
        dialogue.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        responses = dialogue.run()
        if responses == Gtk.ResponseType.OK:
            try:
                filename = dialogue.get_filename()
                tab = Tab(filename, self.tabs)
                self.tabs.append_page(tab, tab.label)
            except UnicodeDecodeError:
                pass
        dialogue.destroy()
        self.show_all()
    
    def saveasTab(self, widget):
        dialogue = Gtk.FileChooserDialog(title="Save As", parent=self, action=Gtk.FileChooserAction.SAVE)
        dialogue.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        responses = dialogue.run()
        if responses == Gtk.ResponseType.OK:
            filename = dialogue.get_filename()
            tab = self.tabs.get_nth_page(self.tabs.get_current_page())
            tab.filename = filename
            tab.label = TabLabel(tab, filename, self.tabs)
            self.tabs.set_tab_label(tab, tab.label)
            with open(filename, "w") as f: 
                f.write(tab.buffer.get_text(tab.buffer.get_start_iter(), tab.buffer.get_end_iter(), True))
        dialogue.destroy()
        self.show_all()
    
    def saveTab(self, widget):
        tab = self.tabs.get_nth_page(self.tabs.get_current_page())
        if tab.filename == "":
            self.saveasTab(widget)
        else:
            with open(tab.filename, "w") as f:
                f.write(tab.buffer.get_text(tab.buffer.get_start_iter(), tab.buffer.get_end_iter(), True))
            self.show_all()

class Tab(Gtk.Grid):
    def __init__(self, filename, notebook):
        Gtk.Grid.__init__(self)
        
        self.scroll = Gtk.ScrolledWindow()
        self.buffer = Gtk.TextBuffer()
        if not filename == "":
            with open(filename, "r") as f:
                self.buffer.set_text(f.read())
            self.label = TabLabel(self, filename, notebook)
        else:
            self.label = TabLabel(self, "New", notebook)
        
        self.filename = filename
        self.text = Gtk.TextView()
        self.text.set_buffer(self.buffer)
        self.text.set_monospace(True)
        self.scroll.add(self.text)
        self.scroll.set_vexpand(True)
        self.scroll.set_hexpand(True)
        self.attach(self.scroll, 0, 0, 2, 2)
        
        self.terminal = Vte.Terminal()
        self.pty = Vte.Pty.new_sync(Vte.PtyFlags.DEFAULT)
        self.pty.set_utf8(True)
        self.terminal.set_pty(self.pty)
        self.pty.spawn_async(
                os.environ["HOME"],
                ["/bin/sh"],
                None,
                GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                None,
                None,
                -1,
                None,
                lambda x, y: x
                )
        self.attach(self.terminal, 0, 2, 2, 1)

class TabLabel(Gtk.Box):
    def __init__(self, tab, name, notebook):
        Gtk.Box.__init__(self)
        
        self.label = Gtk.Label(label=name+" ")
        self.add(self.label)
        self.notebook = notebook
        self.tab = tab
        self.closeBtn = Gtk.Button.new_from_icon_name("window-close", 1)
        self.closeBtn.connect("clicked", self.close)
        self.add(self.closeBtn)
        self.show_all()
    
    def close(self, widget):
        self.notebook.remove_page(self.notebook.page_num(self.tab))

window = Window()
Gtk.main()
