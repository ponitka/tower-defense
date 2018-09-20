import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from queue import Queue
from square import Square

class Board(Gtk.Box):
  
  def __init__(self, maze, player):
    Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL, spacing = 0)

    self.height = maze.height * 2
    self.width = maze.width * 2
    self.maze = maze
    self.player = player

    self.square = []
    for i in range(self.height):
      self.square.append([])
      for j in range(self.width):
        if maze[i//2][j//2] == 1:
          sq = Square(Type = "player")
        else:
          sq = Square(Type = "enemy")
        self.square[i].append(sq)
        sq.update(1, 1)

    for i in range(self.height):
      box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)
      for j in range(self.width):
        box.pack_start(self.square[i][j], True, True, 0)
      self.pack_start(box, True, True, 0)

    self.dist = [[-1 for i in range(self.width)] for j in range(self.height)]

  def inside(self, x, y):
    return (0 <= x and x < self.height) and (0 <= y and y < self.width)

  def __getitem__(self, i):
    return self.square[i]

  def bfs(self, s_x, s_y):
    self.dist = [[-1 for i in range(self.width)] for j in range(self.height)]

    if s_x >= 0:
      self.dist[s_x][s_y] = 0
    else:
      self.dist[-s_x][-s_y] = 0
      for i in range(self.height):
        for j in range(self.width):
          if self[i][j].Type == "enemy":  
            if self[i][j].Occupant != -1:
              self.dist[i][j] = 0

    Q = Queue()
    for i in range(self.height):
      for j in range(self.width):
        if self.dist[i][j] == 0:
          Q.put([i, j])

    while not Q.empty():
      u = Q.get()
      for d in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
        if self.inside(u[0] + d[0], u[1] + d[1]):
          if self.dist[u[0] + d[0]][u[1] + d[1]] == -1:
            if self[u[0] + d[0]][u[1] + d[1]].Type == "enemy":
              self.dist[u[0] + d[0]][u[1] + d[1]] = self.dist[u[0]][u[1]] + 1
              Q.put([u[0] + d[0], u[1] + d[1]])
 
    return True
