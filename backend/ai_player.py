from tensorflow.keras import datasets, layers, models
import numpy as np
import random

class AIPlayer:
  def __init__(self, width, height):
    self.gomoku = 1
    self.model = models.Sequential()
    self.model.add(layers.Conv2D(5, (3, 3), padding='same', activation='relu', input_shape=(15, 15, 3)))

    for i in range(10):
      self.model.add(layers.Conv2D(5, (3, 3), padding='same', activation='relu'))

    self.model.add(layers.Dense(1, activation='softmax'))
    self.model.add(layers.Conv2D(5, (3, 3), padding='same', activation='relu'))

    """
    self.model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    self.model.add(layers.MaxPooling2D((2, 2)))
    """

    #self.model.add(layers.Flatten())

    #self.model.add(layers.Dense((width, height), activation='relu'))
    #self.model.add(layers.Dense(width * height, activation='softmax'))

    self.model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

  def next(self, game):
    board_state = game.board
    #result = self.model.predict(board_state.reshape(1, 15, 15, 3))
    #print(result.shape)
    #result = result.reshape(15 * 15);
    #print(np.argwhere(result == np.amax(result)).flatten())
    return random.randrange(0, 15), random.randrange(0, 15)

  def train(self, board_state):
    self.model.fit(train_images, train_labels, epochs=5)

