import enum
import numpy as np
import tensorflow as tf

class State(enum.Enum):
  kEmpty = 0
  kBlack = 1
  kWhite = 2

class Game(object):
  def __init__(self, width, height):
    self.board = np.zeros((width, height, 3), dtype=int)
  def get_state(self, x, y):
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

def check(game, x, y, func, state):
  count = 0
  while(game.get_state(x,y) == state):
    count = count+1
    x, y = func(x,y)

  return count
 
def is_game_finished(game, x, y):
  state = game.get_state(x, y)
  if (check(game, x, y, front, state) + check(game, x, y, back, state) == 6):
    return True
  return False


