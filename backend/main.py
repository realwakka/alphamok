from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import tensorflow as tf
from ai_player import AIPlayer
from game import Game
from game import State

class TestPlayer:
  def next(self, game):
    game.print_board()
    x = input('x = ')
    y = input('y = ')
    return int(x),int(y)


def play_episode(player1, player2):
  player1.state = State.kBlack
  player2.state = State.kWhite
  game = Game(15, 15)
  
  while(True):
    ret = False
    x = -1
    y = -1

    while(ret == False):
      x, y = player1.next(game)
      ret = game.set_state(x, y, 1)

    if (game.is_finished_move(x, y)):
      game.print_board()
      print('player 1 win!')
      return game

    ret = False
    while(ret == False):
      x, y = player2.next(game)
      ret = game.set_state(x, y, 2)

    if (game.is_finished_move(x, y)):
      game.print_board()
      print('player 2 win!')
      return game

  return None

def main():
  ai_player1 = TestPlayer()
  ai_player2 = AIPlayer(15, 15)
  while True:
    game = play_episode(ai_player1, ai_player2)
    if game != None:
      ai_player1.train_game(game)
      ai_player2.model = ai_player1.model

if __name__ == "__main__":
  main()
  

