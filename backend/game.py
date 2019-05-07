import enum
import numpy as np
import tensorflow as tf

class GameState(enum.Enum):
  kBlackTurn = 0
  kWhiteTurn = 1
  kEndDraw = 2
  kEndBlackWin = 3
  kEndWhiteWin = 4

class State(enum.Enum):
  kEmpty = 0
  kBlack = 1
  kWhite = 2
  def __int__(self):
    return self.value

class Game:
  def __init__(self, width, height):
    self.history = []
    self.board = np.zeros((width, height), dtype=int)
    self.width = width
    self.height = height 

  def get_current_player():
    return len(self.history) % 2 + 1

  def available_move():
    list = []
    for i in range(self.height):
      for j in range(self.width):
        if self.board[j, i, 0] == State.kEmpty:
          list.append({j, i})
    return list

  def move_count(self):
    return len(self.history)
    
  def print_board(self):
    for i in range(self.height):
      for j in range(self.width):
        print(int(self.get_state(j, i)), end=' ')
      print()
   
  def get_state(self, x, y):
    if x >= 0 and x < self.width and y >= 0 and y < self.height:
      return self.board[x, y]
    return -1

  def set_state(self, x, y, state):
    if x >= 0 and x < self.width and y >= 0 and y < self.height:
      self.board[x, y] = state
      self.history.append({x,y})
      return True
    return False
     
  def is_finished(self):
    for i in range(self.height):
      for j in range(self.width):
        if self.is_finished(j, i) == True:
          return True, self.get_state(j,i)

    if self.is_full():
      return True, -1

    return False, -1

  def is_full(self):
    for i in range(self.height):
      for j in range(self.width):
        if self.board[i, j] != State.kEmpty:
          return False

    return True

  def is_finished(self, x, y):
    if self.is_empty(x, y):
      return False
    
    if (self.is_game_finished(x, y, lambda x, y: (x+1, y), lambda x, y: (x-1, y))):
      return True
    if (self.is_game_finished(x, y, lambda x, y: (x, y+1), lambda x, y: (x, y-1))):
      return True
    if (self.is_game_finished(x, y, lambda x, y: (x+1, y+1), lambda x, y: (x-1, y-1))):
      return True
    if (self.is_game_finished(x, y, lambda x, y: (x+1, y-1), lambda x, y: (x-1, y+1))):
      return True

    return False
  def check(self, x, y, func, state):
    count = 0
    while(self.get_state(x,y) == state):
      count = count+1
      x, y = func(x,y)
  
    return count
  def is_empty(self, x, y):
    return self.get_state(x,y) == State.kEmpty

  def is_game_finished(self, x, y, front, back):
    state = self.get_state(x, y)
    front_count = self.check(x, y, front, state)
    back_count = self.check(x, y, back, state)
    if (front_count + back_count == 6):
      return True
    return False

