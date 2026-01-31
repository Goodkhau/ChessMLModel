import tensorflow as tf
from matplotlib import pyplot as plt

model_name = 'Little Blue'
logdir = '..\\log/{model_name}'
batch_size = 128
num_epochs = 10
num_classes = 384

tf.data.Dataset.from_tensors

input = tf.keras.Input(shape=(512,))
first_dense = tf.keras.layers.Dense(1024)(input)
second_dense = tf.keras.layers.Dense(1024)(first_dense)
third_dense = tf.keras.layers.Dense(768)(second_dense)
fourth_dense = tf.keras.layers.Dense(512)(third_dense)
outputs = tf.keras.layers.Dense(num_classes)(fourth_dense)
model = tf.keras.Model(inputs=input, outputs=outputs)

## model.summary()
## sys.exit()

tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)

history = model.fit(train_dataset, num_epochs, validation_data=val, callbacks=[tensorboard_callback])

fig = plt.figure()
plt.plot(history.history['loss'], color='teal', label='loss')
plt.plot(history.history['val_loss'], color='orange', label='val_loss')
fig.suptitle('Loss', fontsize=20)
plt.legend(loc='upper left')
plt.show()
