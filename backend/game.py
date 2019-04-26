import enum
import numpy as np
import tensorflow as tf

class State(enum.Enum):
  kEmpty = 0
  kBlack = 1
  kWhite = 2
  def __int__(self):
    return self.value


class Game(object):
  def __init__(self, width, height):
    self.board = np.zeros((width, height, 3), dtype=int)
    for i in range(height):
      for j in range(width):
        self.board[i, j, 0] = 1

    self.width = width
    self.height = height 
  def print_board(self):
    for i in range(self.height):
      for j in range(self.width):
        print(int(self.get_state(j, i)), end=' ')
      print()


  def get_state(self, x, y):
    if (x < 0 or x >= self.width or y < 0 or y >= self.height):
      return -1
    if (self.board[x, y, 0] == 1):
      return State.kEmpty
    elif (self.board[x, y, 1] == 1):
      return State.kBlack
    elif (self.board[x, y, 2] == 1):
      return State.kWhite

  def set_state(self, x, y, state):
    if (self.board[x, y, 0] == 1):
      self.board[x, y, state] == 1
      return True

    return False
  def is_full(self):
    for i in range(self.height):
      for j in range(self.width):
        if (self.board[i, j, 0] != 1):
          return False

    return True

  def is_finished(self, x, y):
    
    if (self.is_game_finished(x, y, lambda x, y: (x+1, y), lambda x, y: (x-1, y)) == 6):
      return True
    if (self.is_game_finished(x, y, lambda x, y: (x, y+1), lambda x, y: (x, y-1)) == 6):
      return True
    if (self.is_game_finished(x, y, lambda x, y: (x+1, y+1), lambda x, y: (x-1, y-1)) == 6):
      return True
    if (self.is_game_finished(x, y, lambda x, y: (x+1, y-1), lambda x, y: (x-1, y+1)) == 6):
      return True

    if (self.is_full()):
      return True

    return False
  def check(self, x, y, func, state):
    count = 0
    while(self.get_state(x,y) == state):
      count = count+1
      x, y = func(x,y)
  
    return count
 

  def is_game_finished(self, x, y, front, back):
    state = self.get_state(x, y)
    if (self.check(x, y, front, state) + self.check(x, y, back, state) == 6):
      return True
    return False


  
