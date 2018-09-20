import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

class Level(Gtk.Box):

  value = GObject.Property(type = int, default = 0)

  active = "images/star_active.png"
  inactive = "images/star_inactive.png"

  def __init__(self, image):
    Gtk.Box.__init__(self)

    self.pack_start(image, True, True, 0)

    self.array = []
    for i in range(6):
      self.array.append(Gtk.Image.new_from_file(self.inactive))
      self.pack_start(self.array[i], True, True, 0)

    self.connect("notify::value", self.update)

  def update(self, a, b):
    val = self.get_property("value")
    for i in range(val):
      self.array[i].set_from_file(self.active)
    for i in range(val, 6):
      self.array[i].set_from_file(self.inactive)
    self.show()
