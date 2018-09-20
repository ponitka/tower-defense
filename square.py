import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, GdkPixbuf, Gdk, GLib

from enemy import Enemy
from tower import Tower

class Square(Gtk.Box):
  
  path_ground_enemy = "images/ground_enemy.png"
  path_ground_enemy_range = "images/ground_enemy_range.png"
  path_ground_player = "images/ground_player.png"
  gate_image = "images/gate.png"
  
  def __init__(self, Type):
    Gtk.Box.__init__(self)

    self.Type = Type
    self.Occupant = -1
    self.bought = False
    self.gate = False
    self.shoot = False
    self.range = False

    self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.path_ground_player)
    self.image = Gtk.Image.new_from_pixbuf(self.pixbuf)
    #self.pack_start(self.image, True, True, 0)
    self.image.connect('size-allocate', self.update)
  
    self.overlay = Gtk.Overlay()
    self.add(self.overlay)
    self.overlay.add(self.image)

    self.label = Gtk.Label("")
    self.overlay.add_overlay(self.label)

  def update(self, a, b):
    path = -1

    if self.Type == "player":
      if self.Occupant == -1:
        path = self.path_ground_player
      else:
        if self.bought == True:
          if self.shoot == True:
            path = self.Occupant.path_shoot
          else:
            path = self.Occupant.path_active
        else:
          path = self.Occupant.path_inactive

    if self.Type == "enemy":
      if self.gate == True:
        path = self.gate_image
      else:
        if self.Occupant == -1:
          if self.range == True:
            path = self.path_ground_enemy_range
          else:
            path = self.path_ground_enemy
        else:
          if self.range == True:
            path = self.Occupant.path_range
          else:
            path = self.Occupant.path
  
    allocation = self.get_allocation()
    self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(path)
    self.pixbuf = self.pixbuf.scale_simple(max(16, allocation.width), max(16, allocation.height), GdkPixbuf.InterpType.HYPER)
    self.image.set_from_pixbuf(self.pixbuf)
