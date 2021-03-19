import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Ahead")
        self.connect("destroy", Gtk.main_quit)
        self.set_size_request(600, 400)
        
        self.left_panel = Gtk.Notebook()
        self.left_panel.set_tab_pos(Gtk.PositionType.LEFT)
        self.add(self.left_panel)
        self.edit = Gtk.VBox()
        
        self.tabs = Gtk.Notebook(expand=True)
        self.tabs.set_scrollable(True)
        self.tabs.connect("change-current-page", self.change_page)
        self.edit.add(self.tabs)
        
        self.left_panel.append_page(self.edit, Gtk.Label(label="Edit"))
        
        self.tab = Tab(self.tabs, "Tab")
        self.label = TabLabel(self.tab, "Tab", self.tabs)
        self.tabs.append_page(self.tab, self.label)
        
        self.tabs.append_page(Gtk.VBox(), Gtk.Image.new_from_icon_name("help-about", 1))
        
        self.show_all()
    
    def change_page(self, notebook, num):
        print(num)

class Tab(Gtk.ScrolledWindow):
    def __init__(self, notebook, name):
        Gtk.ScrolledWindow.__init__(self)

        self.text = Gtk.TextView()
        self.text.set_monospace(True)
        self.add(self.text)

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
        self.notebook.reorder_child(self.tab, -1)
        self.notebook.remove_page(-1)

window = Window()
Gtk.main()