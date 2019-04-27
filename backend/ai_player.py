from tensorflow.keras import datasets, layers, models
import numpy as np
import random

class AIPlayer:
  def __init__(self, width, height):
    self.model = models.Sequential()
    self.model.add(layers.Conv2D(32, (5, 5), padding='same', activation='relu', input_shape=(15, 15, 3)))

    for i in range(10):
      self.model.add(layers.Conv2D(192, (3, 3), padding='same', activation='relu'))

    self.model.add(layers.Conv2D(192, (1, 1), padding='same', activation='relu'))
    self.model.add(layers.Flatten())
    self.model.add(layers.Dense(256, activation='relu'))
    self.model.add(layers.Dense(1, activation='softmax'))

    """
    self.model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    self.model.add(layers.MaxPooling2D((2, 2)))


    self.model.add(layers.Dense((width, height), activation='relu'))
    self.model.add(layers.Dense(width * height, activation='softmax'))
    """

    self.model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

  def get_winning_rate(self, x, y, board):
    tmp_board = np.copy(board)
    tmp_board[x, y, int(self.state)] = 1
    tmp_board[x, y, 0] = 0
    result = self.model.predict(board.reshape(1, 15, 15, 3))
    return result 

  def next(self, game):
    max_rate = -1
    best_list = []
    max_x = -1
    max_y = -1
    for i in range(game.height):
      for j in range(game.width):
        if game.is_empty(i, j):
          if self.get_winning_rate(j, i, game.board) > max_rate:
            best_list.append([j, i])
    
    best_next = best_list[random.randrange(len(best_list))]

    print('selected x = ' + str(best_next[0]) + ' selected y = ' + str(best_next[1]))
    print('max rate = ' + str(max_rate))
    return best_next[0], best_next[1]
          
    while True:
      result = self.model.predict(game.board.reshape(1, 15, 15, 3))
      result = result.reshape(15,15)
      max_indices = np.argwhere(result == np.amax(result))

      selected = random.randrange(0, max_indices.shape[0])
      x = max_indices[selected][0]
      y = max_indices[selected][1]
      if (game.is_empty(x,y)):
        return x,y
      game.print_board()
      input('failed')
      result[x,y] = 0
      self.train(game.board.reshape(1, 15,15, 3), result.reshape(1, 15, 15, 1))
      
  def train_game(self, game):
    count = game.move_count()
    board_data = np.zeros(count, 15, 15, 3)
    result = np.zeros(count)
    i = 0
    for elem in game.history:
        board_data[i, elem[0], elem[1], (i%2) + 1] = 1
        if i%2 == count%2:
          result[i] = 1
        else:
          result[i] = 0
        i = i + 1
    self.model.fit(board_data, result, epochs=5)
      
  def train(self, state, result):
    self.model.fit(state, result, epochs=5)
