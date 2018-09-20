import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from tower import Tower

class Towers:
  
  def __init__(self, board, sidebar, player, enemies):
    towers = []
    self.board = board
    self.sidebar = sidebar
    self.player = player
    self.enemies = enemies

  def buy_tower(self):
    if self.player.game_is_running == False:
      return False
    
    if self.player.budget < self.player.tower.cost:
      return False
    if self.board[self.player.pos_x][self.player.pos_y].bought == True:
      return False
  
    self.player.budget -= self.player.tower.cost
    self.sidebar.update()

    for to in self.sidebar.towers:
      self.sidebar.remove(to)

    self.player.tower.pos_x = self.player.pos_x
    self.player.tower.pos_y = self.player.pos_y
    self.board[self.player.pos_x][self.player.pos_y].bought = True
    self.board[self.player.pos_x][self.player.pos_y].update(1, 1)
    GObject.timeout_add(1000 // self.player.tower.spee, self.shoot, self.player.tower)
    self.board[self.player.tower.pos_x][self.player.tower.pos_y].label.set_markup("<span color='red'>%d</span>" % self.player.tower.rang)

    self.new_tower = Tower(self.player.tower.indx, self.player.tower.rang, self.player.tower.spee, self.player.tower.cost)
    self.sidebar.towers[self.player.tower.indx] = self.new_tower
    self.sidebar.towers[self.player.tower.indx].set_property("active", True)
    self.new_tower.show_all()
  
    for to in self.sidebar.towers:
      self.sidebar.pack_start(to, True, True, 0)

    self.player.tower = self.new_tower

    return True

  def change_shoot(self, tower, val):
    self.board[tower.pos_x][tower.pos_y].shoot = val
    self.board[tower.pos_x][tower.pos_y].update(1, 1)
    self.board[tower.pos_x][tower.pos_y].show()
    return False

  def shoot(self, tower):
    if self.player.game_is_running == False:
      return False

    self.change_shoot(tower, True)
    GObject.timeout_add(100, self.change_shoot, tower, False)

    to_shoot = []
    for ii in range(-tower.rang, tower.rang+1):
      for jj in range(-tower.rang, tower.rang+1):
        if abs(ii) + abs(jj) <= tower.rang:
          if self.board.inside(tower.pos_x + ii, tower.pos_y + jj):
            square = self.board[tower.pos_x + ii][tower.pos_y + jj]
            if square.Type == "enemy":
              if square.Occupant != -1:
                if square.gate == False:
                  Dist = self.board.dist[tower.pos_x + ii][tower.pos_y + jj]
                  to_shoot.append([Dist, [tower.pos_x + ii, tower.pos_y + jj]])

    if len(to_shoot) > 0:
      to_shoot.sort()
      self.enemies.kill(self.board[to_shoot[0][1][0]][to_shoot[0][1][1]].Occupant)

    return True
