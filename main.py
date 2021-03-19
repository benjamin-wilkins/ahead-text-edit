import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Ahead")
        self.connect("destroy", Gtk.main_quit)
        self.set_size_request(600, 400)
        
        self.titlebar = Gtk.HeaderBar()
        self.titlebar.set_show_close_button(True)
        self.titlebar.props.title = "Ahead"
        
        self.toolbarBox = Gtk.HBox()
        Gtk.StyleContext.add_class(self.toolbarBox.get_style_context(), "linked")
        
        self.open = Gtk.Button(label="Open")
        self.toolbarBox.add(self.open)
        
        self.save = Gtk.Button(label="Save")
        self.toolbarBox.add(self.save)
        
        self.saveas = Gtk.Button(label="Save As")
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
        
        tab = Tab("")
        label = TabLabel(tab, "New", self.tabs)
        self.tabs.append_page(tab, label)
        
        self.left_panel.append_page(self.edit, Gtk.Label(label="Edit"))
        
        self.show_all()
    
    def newTab(self, widget):
        print("New tab")
        tab = Tab("")
        label = TabLabel(tab, "New", self.tabs)
        self.tabs.append_page(tab, label)
        self.show_all()
    
class Tab(Gtk.ScrolledWindow):
    def __init__(self, filename):
        Gtk.ScrolledWindow.__init__(self)

        self.text = Gtk.TextView()
        self.text.set_monospace(True)
        self.add(self.text)

class TabLabel(Gtk.Box):
    def __init__(self, tab, name, notebook):
        Gtk.Box.__init__(self)
        
        self.label = Gtk.Label(label=name+"  ")
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