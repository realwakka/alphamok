from tensorflow.keras import datasets, layers, models, regularizers, Input, optimizers
import numpy as np
import random
from mcts import MCTS
from game import Game

def create_input(game):
  current = game.current_player()
  input_data = np.zeros((4, game.width, game.height))

  input_data[2][game.last_move()] = 1

  for i in range(game.height):
    for j in range(game.width):
      state = game.get_state()
      input_data[0][j, i] = 1
      input_data[3][j, i] = state
      if state == State.kEmpty:
        input_data[0][j,i] = 0
      elif state == current:
        input_data[0][j,i] = 1
      else:
        input_data[1][j,i] = 1
        if game.last_move() == {j,i}:
          input_data[2][j,i] = 1

  return input_data

class AIPlayer:
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.l2_const = 1e-4  # coef of l2 penalty
    in_x = network = Input((4, self.width, self.height))
    network = layers.Conv2D(filters=32, kernel_size=(3, 3), padding="same", data_format="channels_first", activation="relu", kernel_regularizer=regularizers.l2(self.l2_const))(network)
    network = layers.Conv2D(filters=64, kernel_size=(3, 3), padding="same", data_format="channels_first", activation="relu", kernel_regularizer=regularizers.l2(self.l2_const))(network)
    network = layers.Conv2D(filters=128, kernel_size=(3, 3), padding="same", data_format="channels_first", activation="relu", kernel_regularizer=regularizers.l2(self.l2_const))(network)
    # action policy layers
    policy_net = layers.Conv2D(filters=4, kernel_size=(1, 1), data_format="channels_first", activation="relu", kernel_regularizer=regularizers.l2(self.l2_const))(network)
    policy_net = layers.Flatten()(policy_net)
    self.policy_net = layers.Dense(self.width*self.height, activation="softmax", kernel_regularizer=regularizers.l2(self.l2_const))(policy_net)
    # state value layers
    value_net = layers.Conv2D(filters=2, kernel_size=(1, 1), data_format="channels_first", activation="relu", kernel_regularizer=regularizers.l2(self.l2_const))(network)
    value_net = layers.Flatten()(value_net)
    value_net = layers.Dense(64, kernel_regularizer=regularizers.l2(self.l2_const))(value_net)
    self.value_net = layers.Dense(1, activation="tanh", kernel_regularizer=regularizers.l2(self.l2_const))(value_net)

    self.model = models.Model(in_x, [self.policy_net, self.value_net])

    opt = optimizers.Adam()
    losses = ['categorical_crossentropy', 'mean_squared_error']
    self.model.compile(optimizer=opt, loss=losses)
    self.mcts = MCTS(self.policy_value, 5, 400)

  def next(self, game):
    acts, probs = self.mcts.get_move_probs(game, 1e-3)
    move_probs = np.zeros(game.width*game.height)
    move = np.random.choice(acts, p=0.75*probs + 0.25*np.random.dirichlet(0.3*np.ones(len(probs))))
    return move

  def policy_value(self, board):
    input_data = create_input(game)
    legal_positions = board.availables()
    current_state = board.current_state()
    state_input_union = np.array(state_input)
    act_probs, value = self.model.predict(input_data)
    act_probs = zip(legal_positions, act_probs.flatten()[legal_positions])
    return act_probs, value[0][0]

  def next(self, game):
    result = self.model.predict(game.board.reshape(1, self.width, self.height, 3))
    result = result.reshape(self.width * self.height)
    indices = np.argsort(result)
    i = self.width * self.height - 1

    while True:
      x = indices[i] % self.width
      y = indices[i] // self.width

      if game.is_empty(x, y):
        return x, y

      if i == 0:
        break;
      i -= 1
    raise Exception('full!')

