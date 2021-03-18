import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Ahead")
        self.connect("destroy", Gtk.main_quit)
        
        self.left_panel = Gtk.Notebook()
        self.left_panel.set_tab_pos(Gtk.PositionType.LEFT)
        self.add(self.left_panel)
        
        self.tabs = Gtk.Notebook()
        self.left_panel.append_page(self.tabs, Gtk.Label(label="Edit"))
        
        self.tabs.append_page(Tab(), Gtk.Label(label="Tab"))
        
        self.show_all()

class Tab(Gtk.TextView):
    def __init__(self):
        Gtk.TextView.__init__(self)
        
        self.modify_font(Pango.FontDescription("monospace"))

window = Window()
Gtk.main()