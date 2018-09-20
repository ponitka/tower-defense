import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

import random
from enemy import Enemy

class Enemies:

  def __init__(self, board, sidebar, player):
    self.enemies = []
    self.board = board
    self.sidebar = sidebar
    self.player = player
    self.source = [-1, -1]
    self.aim = [-1, -1]

  def NewEnemy(self, x, y, health, velocity):
    if self.board.inside(x, y) == False or self.board[x][y].Type == "player" or self.board[x][y].Occupant != -1:
      return False
    self.enemies.append(Enemy(x, y, len(self.enemies), health, velocity))

    self.board[x][y].Occupant = self.enemies[-1]
    self.board[x][y].update(1, 1)
    self.board[x][y].label.set_markup("<span color='yellow'>%d</span>" % health)

    self.FindMove(self.enemies[-1])
    GObject.timeout_add(1000 // self.enemies[-1].velocity, self.FindMove, self.enemies[-1])
    return False

  def MakeWave(self):
    if self.player.game_is_running == False:
      return False
    
    self.player.waves += 1
    self.sidebar.update()
    
    x, y = 0, 0
    while self.board[x][y].Type == "player" or self.board[x][y].Occupant != -1: 
      x = random.randint(0, self.board.height-1)
      y = random.randint(0, self.board.width-1)
    self.source = [x, y]

    self.board[self.aim[0]][self.aim[1]].gate = False
    self.board[self.aim[0]][self.aim[1]].update(1, 1)
  
    self.board.bfs(-x, -y)

    possible_zt = []
    for i in range(self.board.height):
      for j in range(self.board.width):
        if self.board[i][j].Type == "enemy":
          if self.board[i][j].Occupant == -1:
            possible_zt.append([self.board.dist[i][j], [i, j]])

    possible_zt.sort(reverse = True)
    indx = random.randint(0, (len(possible_zt) // 4) + 1)
    z, t = possible_zt[indx][1][0], possible_zt[indx][1][1]
    self.aim = [z, t]
    
    self.board[self.aim[0]][self.aim[1]].gate = True
    self.board[self.aim[0]][self.aim[1]].update(1, 1)

    self.board.bfs(z, t)

    GObject.timeout_add(1000, self.NewEnemy, x, y, 1 * self.player.waves, 4)
    GObject.timeout_add(2000, self.NewEnemy, x, y, 1 * self.player.waves, 8)
    GObject.timeout_add(3500, self.NewEnemy, x, y, 1 * self.player.waves, 8)

    return True

  def Win(self, enemy):
    self.player.budget -= enemy.cost
    self.sidebar.update()
    self.board[enemy.pos_x][enemy.pos_y].Occupant = -1
    self.board[enemy.pos_x][enemy.pos_y].update(1, 1)
    enemy.status = "won"

    if self.player.budget < 0:
      self.player.game_is_running = False

  def MakeMove(self, enemy, x, y):
    if abs(enemy.pos_x - x) + abs(enemy.pos_y - y) != 1:
      return False
    if self.board[x][y].Type != "enemy" or self.board[x][y].Occupant != -1:
      return False

    self.board[enemy.pos_x][enemy.pos_y].label.set_markup("")

    self.board[x][y].Occupant = enemy
    self.board[enemy.pos_x][enemy.pos_y].Occupant = -1

    self.board[x][y].update(1, 1)
    self.board[enemy.pos_x][enemy.pos_y].update(1, 1)

    enemy.pos_x, enemy.pos_y = x, y

    if self.board[enemy.pos_x][enemy.pos_y].gate == True:
      self.Win(enemy)      
    else:
      self.board[enemy.pos_x][enemy.pos_y].label.set_markup("<span color='yellow'>%d</span>" % enemy.health)

    return True

  def FindMove(self, enemy):
    if enemy.status != "alive":
      return False
    if self.player.game_is_running == False:
      return False

    best_value = 1000000
    solutions = []

    for d in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
      if self.board.inside(enemy.pos_x + d[0], enemy.pos_y + d[1]):
        if self.board[enemy.pos_x + d[0]][enemy.pos_y + d[1]].Occupant == -1:
          dist = self.board.dist[enemy.pos_x + d[0]][enemy.pos_y + d[1]]
          if dist != -1:
            new_move = dist
            if new_move < best_value:
              best_value = new_move
              solutions.clear()
            if new_move == best_value:
              solutions.append(d)

    random.shuffle(solutions)
    if len(solutions) > 0:
      self.MakeMove(enemy, enemy.pos_x + solutions[0][0], enemy.pos_y + solutions[0][1])
    
    return True

  def kill(self, enemy):
    enemy.health -= 1
    
    if enemy.health == 0:
      enemy.status = "dead"
      self.player.budget += enemy.cost
      self.sidebar.update()
      self.board[enemy.pos_x][enemy.pos_y].Occupant = -1
      self.board[enemy.pos_x][enemy.pos_y].label.set_markup("")
      self.board[enemy.pos_x][enemy.pos_y].update(1, 1)
    else:
      self.board[enemy.pos_x][enemy.pos_y].label.set_markup("<span color='yellow'>%d</span>" % enemy.health)
