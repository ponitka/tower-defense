import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Enemy:

  path = "images/enemy.png"
  path_range = "images/enemy_range.png"

  def __init__(self, x, y, index, health, velocity):
    self.pos_x = x
    self.pos_y = y
    self.status = "alive"
    self.index = index
    self.cost = 1

    self.health = health
    self.velocity = velocity
