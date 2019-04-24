from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import tensorflow as tf
from ai_player import AIPlayer
from game import Game

def play_episode(player1, player2):
  game = Game(15, 15)

  game.set_state(0, 0, 1)
  game.get_state(0, 0)


def main():
  ai_player1 = AIPlayer(15, 15)
  ai_player2 = AIPlayer(15, 15)
  play_episode(ai_player1, ai_player2)

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
  

