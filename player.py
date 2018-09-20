import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from tower import Tower

class Player:

  def __init__(self):
    self.pos_x = 0
    self.pos_y = 0
    self.budget = 10

    self.tower = -1
    self.board = -1

    self.sidebar = -1

    self.game_is_running = True
    self.waves = 0

  def move(self, dx, dy):
    if self.board.inside(self.pos_x + dx, self.pos_y + dy) == False:
      return False
    if self.board[self.pos_x + dx][self.pos_y + dy].Type != "player":
      return False
  
    self.range(False)

    old_square = self.board[self.pos_x][self.pos_y]
    if old_square.Occupant == self.tower:
      old_square.Occupant = -1
    old_square.update(1, 1)

    self.pos_x += dx
    self.pos_y += dy

    new_square = self.board[self.pos_x][self.pos_y]
    if new_square.Occupant == -1:
      new_square.Occupant = self.tower
    new_square.update(1, 1)

    self.range(True)

    return True

  def range(self, state):
    if self.tower != -1:
      for ii in range(-self.tower.rang, self.tower.rang+1):
        for jj in range(-self.tower.rang, self.tower.rang+1):
          if abs(ii) + abs(jj) <= self.tower.rang:
            if self.board.inside(self.pos_x + ii, self.pos_y + jj):
              square = self.board[self.pos_x + ii][self.pos_y + jj]
              square.range = state
              square.update(1, 1)
