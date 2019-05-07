from tensorflow.keras import datasets, layers, models, regularizers, Input, optimizers
import numpy as np
import random
from mcts import MCTS
from game import Game, State

def create_input(game):
  current = game.current_player()
  input_data = np.zeros((game.width, game.height, 4))
  
  # set last move
  input_data[game.last_move()[0], game.last_move()[1], 2] = 1

  for i in range(game.height):
    for j in range(game.width):
      state = game.get_state(j, i)
      input_data[j, i][0] = 1
      input_data[j, i][0] = state
      if state == State.kEmpty:
        input_data[j,i][0] = 0
      elif state == current:
        input_data[j,i][0] = 1
      else:
        input_data[j,i][1] = 1
        if game.last_move() == (j,i):
          input_data[j,i][2] = 1

  return input_data

class AIPlayer:
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.l2_const = 1e-4  # coef of l2 penalty
    regularizer = regularizers.l2(self.l2_const)
    in_x = network = Input((width, height, 4))
    network = layers.Conv2D(filters=32, kernel_size=(3, 3), padding="same",
                            data_format="channels_last", activation="relu",
                            kernel_regularizer=regularizer)(network)
    network = layers.Conv2D(filters=64, kernel_size=(3, 3), padding="same",
                            data_format="channels_last", activation="relu",
                            kernel_regularizer=regularizer)(network)
    network = layers.Conv2D(filters=128, kernel_size=(3, 3), padding="same",
                            data_format="channels_last", activation="relu",
                            kernel_regularizer=regularizer)(network)
    
    # action policy layers
    policy_net = layers.Conv2D(filters=4, kernel_size=(1, 1),
                               data_format="channels_last", activation="relu",
                               kernel_regularizer=regularizer)(network)
    policy_net = layers.Flatten()(policy_net)
    self.policy_net = layers.Dense(self.width*self.height, activation="softmax",
                                   kernel_regularizer=regularizer)(policy_net)
    
    # state value layers
    value_net = layers.Conv2D(filters=2, kernel_size=(1, 1),
                              data_format="channels_last", activation="relu",
                              kernel_regularizer=regularizer)(network)
    value_net = layers.Flatten()(value_net)
    value_net = layers.Dense(64, kernel_regularizer=regularizer)(value_net)
    self.value_net = layers.Dense(1, activation="tanh",
                                  kernel_regularizer=regularizer)(value_net)

    self.model = models.Model(in_x, [self.policy_net, self.value_net])
    
    opt = optimizers.Adam()
    losses = ['categorical_crossentropy', 'mean_squared_error']
    self.model.compile(optimizer=opt, loss=losses)
    self.mcts = MCTS(self.policy_value, 5, 400)

  def next(self, game):
    acts, probs = self.mcts.get_move_probs(game, 1e-3)
    p = 0.75*probs + 0.25*np.random.dirichlet(0.3*np.ones(len(probs)))
    move = acts[np.random.choice(len(acts), replace=False, p = p)]
    return move

  def policy_value(self, game):
    input_data = create_input(game).reshape(1, 15, 15, 4)
    legal_positions = game.availables()
    act_probs, value = self.model.predict(input_data)
    act_probs = zip(legal_positions, act_probs.flatten()[legal_positions])
    return act_probs, value[0][0]
