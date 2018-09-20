import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject

import random
from level import Level

class Tower(Gtk.Box):
 
  path_active = "images/tower_active.png"
  path_inactive = "images/tower_inactive.png"
  path_shoot = "images/tower_shoot.png"
  path_range = "images/range.png"
  path_time = "images/time.png"
  path_cost = "images/cost.png"
  
  active = GObject.Property(type = bool, default = False)

  def __init__(self, indx, rang, spee, cost):
    Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL, spacing = 5)

    self.pos_x = -1
    self.pos_y = -1

    self.indx = indx
    self.rang = rang
    self.spee = spee
    self.cost = cost

    self.label = Gtk.Label("Tower %d" % (self.indx + 1))
    self.pack_start(self.label, True, True, 0)

    self.levels = []
    self.image1 = Gtk.Image.new_from_file(self.path_range)
    self.levels.append(Level(self.image1))
    self.image2 = Gtk.Image.new_from_file(self.path_time)
    self.levels.append(Level(self.image2))
    self.image3 = Gtk.Image.new_from_file(self.path_cost)
    self.levels.append(Level(self.image3))

    for i in self.levels:
      self.pack_start(i, True, True, 0)
     
    self.levels[0].set_property("value", self.rang)
    self.levels[1].set_property("value", self.spee)
    self.levels[2].set_property("value", self.cost)
    
    self.change_color("aqua")

    self.connect("notify::active", self.update)

  def change_color(self, color):
    coolor = Gdk.color_parse(color)
    rgba = Gdk.RGBA.from_color(coolor)
    self.override_background_color(0, rgba)

  def update(self, a, b):
    if self.get_property("active") == True:
      self.change_color("dodgerblue")
    else:
      self.change_color("aqua")
