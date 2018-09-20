import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject

from board import Board
from sidebar import Sidebar
from enemies import Enemies
from towers import Towers

class GameWindow(Gtk.Window):
  
  def __init__(self, maze, player):
    Gtk.Window.__init__(self)
    self.set_border_width(20)

    self.bigbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 20)
    self.add(self.bigbox)
    self.label = Gtk.Label(""" Usage of towers: WASD for moving, Q for buying, arrows for changing.
    New wave comes every 15 seconds. You'll lose when your budget becomes negative.
    By killing an enemy you earn 1$, by letting an enemy reach the star you lose 2$. """)
    
    self.label.set_justify(Gtk.Justification.CENTER)
    self.bigbox.pack_start(self.label, True, True, 0)

    self.box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)
    self.bigbox.pack_start(self.box, True, True, 0)

    self.board = Board(maze, player)
    self.box.pack_start(self.board, True, True, 0)

    self.player = player
    self.player.board = self.board

    self.sidebar = Sidebar(self.player, self.board)
    self.box.pack_start(self.sidebar, True, True, 0)

    self.connect("key-press-event", self.press)

    self.board[self.player.pos_x][self.player.pos_y].Occupant = self.player.tower
    self.board[self.player.pos_x][self.player.pos_y].update(1, 1)

    self.enemies = Enemies(self.board, self.sidebar, self.player)
    self.add_bots()
    GObject.timeout_add(15000, self.add_bots)

    self.towers = Towers(self.board, self.sidebar, self.player, self.enemies)

  def add_bots(self):
    self.enemies.MakeWave()
    return True

  def press(self, widget, event):
    keyval = event.keyval
    keyval_name = Gdk.keyval_name(keyval)
    state = event.state

    if keyval_name == "Up":
      self.sidebar.move(-1)
    if keyval_name == "Down":
      self.sidebar.move(+1)

    if keyval_name == "w":
      self.player.move(-1, 0)
    if keyval_name == "s":
      self.player.move(+1, 0)
    if keyval_name == "d":
      self.player.move(0, +1)
    if keyval_name == "a":
      self.player.move(0, -1)

    if keyval_name == "q":
      self.towers.buy_tower()
