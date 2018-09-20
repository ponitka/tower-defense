import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from game import GameWindow
from maze import Maze
from player import Player

player = Player()

maze = Maze(19, 21)
game = GameWindow(maze, player)

game.connect("destroy", Gtk.main_quit)
game.show_all()
Gtk.main()
