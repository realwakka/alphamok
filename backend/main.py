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

    if (game.is_finished(x, y)):
      game.print_board()
      return game

    ret = False
    while(ret == False):
      x, y = player2.next(game)
      ret = game.set_state(x, y, 2)

    if (game.is_finished(x, y)):
      game.print_board()
      return game

  return None

def main():
  ai_player1 = AIPlayer(15, 15)
  ai_player2 = AIPlayer(15, 15)
  game = play_episode(ai_player1, ai_player2)
  if game != None:
    ai_player1.train_game(game)
    ai_player2.model = ai_player1.model

  game = play_episode(ai_player1, ai_player2)


"""
  with tf.Session() as sess:
  sess.run(init)
  for i in num_episodes:
    s = env.reset()
    e = 1 / (( i/50) + 10)
    rAll = 0
    done = False
    local_loss = []
    while not done:
      Qs = sess.run(Qpred, feed_dict={X: one_hot(s)})
      if np.random.rand(1) > e:
	a = env.action_space.sample()
      else:
	a = np.argmax(Qs)

      s1, reward, done, _ = env.step(a)
      if done:
	Qs[0, a] = reward
      else
	Qs1 = sess.run(Qpred, feed_dict={X: one_hot(s1)})
	Qs[0, a] = reward + dis * np.max(Qs1)

      sess.run(train, feed_dict={X: one_hot(s), Y: Qs})
      rAll += reward
      s = s1

    rList.append(rAll)
"""

if __name__ == "__main__":
  main()
  

