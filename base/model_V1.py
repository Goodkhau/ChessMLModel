import tensorflow as tf
from tensorflow import keras
import numpy as np


## taken from geeksforgeeks, need to read up on the different layers.
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (1, 1), activation='relu', input_shape=(24, 24, 1)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu')
])