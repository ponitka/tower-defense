import random

class Maze:
  
  def __init__(self, height, width):
    self.height = height
    self.width = width
    self.array = [[0 for i in range(self.width)] for j in range(self.height)]

    self.borders = []
    for i in range(self.width):
      if (i != 0 and i != self.width-1):
        self.array[0][i] = 1
        if (0 % 2 == 0 and i % 2 == 0):
          self.borders.append([0, i])
      if (i != 0 and i != self.width-1):
        self.array[self.height-1][i] = 1
        if ((self.height-1) % 2 == 0 and i % 2 == 0):
          self.borders.append([self.height-1, i])

    for i in range(self.height):
      self.array[i][0] = 1
      self.array[i][self.width-1] = 1
      if (i % 2 == 0 and 0 % 2 == 0):
        self.borders.append([i, 0])
      if (i % 2 == 0 and (self.width-1) % 2 == 0):
        self.borders.append([i, self.width-1])

    for i in range(self.height):
      for j in range(self.width):
        if (i % 2 == 0 and j % 2 == 0):
          self.array[i][j] = 1   

    self.visited = [[0 for i in range(self.width)] for j in range(self.height)]
    for bo in self.borders:
      self.visited[bo[0]][bo[1]] = 1

    random.shuffle(self.borders)
    for bo in self.borders:
      self.dfs(bo, False)

    rest = []
    for i in range(self.height):
      for j in range(self.width):
        if (i % 2 == 0 and j % 2 == 0):
          if self.visited[i][j] == False:
            for d in [[0, 2], [2, 0], [0, -2], [-2, 0]]:
              if self.inside(i + d[0], j + d[1]):
                if self.visited[i + d[0]][j + d[1]] == True:
                  self.array[i + d[0]//2][j + d[1]//2] = 1
                  self.visited[i][j] = True
                  break
  
  def dfs(self, pos, stop):
    self.visited[pos[0]][pos[1]] = 1

    if stop == True and random.randint(1, 3 * max(self.height, self.width)) == 1:
      return

    ds = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    random.shuffle(ds)

    for d in ds:
     if self.inside(pos[0] + 2*d[0], pos[1] + 2*d[1]):
        if not self.visited[pos[0] + 2*d[0]][pos[1] + 2*d[1]]:
          self.array[pos[0] + d[0]][pos[1] + d[1]] = 1    
          self.dfs([pos[0] + 2*d[0], pos[1] + 2*d[1]], True)
          if stop == True:
            return
          
  def inside(self, i, j):
    if 0 > i or i >= self.height:
      return False
    if 0 > j or j >= self.width:
      return False
    return True

  def __getitem__(self, i):
    return self.array[i]
