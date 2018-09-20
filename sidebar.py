import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from tower import Tower

class Sidebar(Gtk.Box):

  def __init__(self, player, board):
    Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL, spacing = 10)

    self.player = player
    self.player.sidebar = self
    self.board = board

    self.money_label = Gtk.Label("Budget: %d$" % self.player.budget)
    self.pack_start(self.money_label, True, True, 0)

    self.wave_label = Gtk.Label("Waves: %d" % self.player.waves)
    self.pack_start(self.wave_label, True, True, 0)

    self.towers = []
    self.towers.append(Tower(0, 3, 1, 2))
    self.towers.append(Tower(1, 2, 3, 3))
    self.towers.append(Tower(2, 3, 2, 3))
    self.towers.append(Tower(3, 6, 1, 5))

    self.towers[0].set_property("active", True)
    self.active = 0
    self.player.tower = self.towers[0]
    self.player.range(True)

    for to in self.towers:
      self.pack_start(to, True, True, 0)

  def move(self, change):
    self.player.range(False)

    self.towers[self.active].set_property("active", False)
    self.active += change
    self.active = (self.active + len(self.towers)) % len(self.towers)
    self.towers[self.active].set_property("active", True)

    old_tower = self.player.tower
    self.player.tower = self.towers[self.active]

    square = self.board[self.player.pos_x][self.player.pos_y]
    if square.Occupant == old_tower:
      square.Occupant = self.player.tower
      square.update(1, 1)

    self.player.range(True)

  def update(self):
    self.money_label.set_label("Budget: %d$" % self.player.budget)
    self.wave_label.set_label("Waves: %d" % self.player.waves)
