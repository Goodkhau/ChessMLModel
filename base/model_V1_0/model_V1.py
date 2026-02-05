import tensorflow as tf
import sys
from matplotlib import pyplot as plt


MODEL_NAME = 'Little Blue'
LOGDIR = '../log/{MODEL_NAME}'
BATCH_SIZE = 128
NUM_EPOCS = 10
NUM_CLASSES = 384


dataset = tf.data.Dataset.from_tensor_slices([[[1,2],[3,4],[5,6],[7,8]],[[1,2],[3,4],[5,6],[7,8]],[[1,2],[3,4],[5,6],[7,8]]])
for element in dataset:
    print(element)
sys.exit()
tf.Tensor

input = tf.keras.Input(shape=(512,))
first_dense = tf.keras.layers.Dense(1024)(input)
second_dense = tf.keras.layers.Dense(1024)(first_dense)
third_dense = tf.keras.layers.Dense(768)(second_dense)
fourth_dense = tf.keras.layers.Dense(512)(third_dense)
outputs = tf.keras.layers.Dense(NUM_CLASSES)(fourth_dense)
model = tf.keras.Model(inputs=input, outputs=outputs, name=MODEL_NAME)

## model.summary()
## sys.exit()

tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=LOGDIR)

history = model.fit(train_dataset, NUM_EPOCS, validation_data=val, callbacks=[tensorboard_callback])

fig = plt.figure()
plt.plot(history.history['loss'], color='teal', label='loss')
plt.plot(history.history['val_loss'], color='orange', label='val_loss')
fig.suptitle('Loss', fontsize=20)
plt.legend(loc='upper left')
plt.show()
