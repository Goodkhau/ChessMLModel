import tensorflow as tf
from data.DataPipeline import populate_training_data
from base.model_V1_0.model_V1 import model_V1


def valid_selection(selection: int) -> bool:
    return False if selection < 0 or selection > 3 else True

def get_selection(selection: int = -1) -> int:
    PROMPT: str = f"Select an option\n1: Load and Partition Dataset.\n2: Select Model.\n3: Train and Output Model.\n"

    while (not valid_selection(selection)):
        try:
            selection = int(input(PROMPT))
            if not valid_selection(selection):
                raise ValueError()
        except:
            print("Invalid selection.\n")

    return selection


if __name__ == "__main__":
    selection: int = -1
    while (selection):
        model: None | tf.keras.Model[tf.Tensor, tf.Tensor] = None
        match (selection):
            case 1:
                populate_training_data('my_model')
            case 2:
                model = model_V1().model
                model.summary()
            case 3:
                if not model:
                    print("Model not selected.\n")
                    continue
            case _:
                selection = get_selection()
    print("Exiting.\n")
    # for game in dataset['train']:
    #     format: TrainingData = TrainingData(game['moves_san'])
    #     #data: tf.data.Dataset[tf.Tensor] = tf.data.Dataset.from_tensor_slices(format.san_to_tensorslices(), name=MODEL_NAME)
    #     for tensor in format.san_to_feature_tensorslices():
    #         print(tensor)
    #     break

    ## model.summary()
    ## sys.exit()

# tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=LOGDIR)

# history = model.fit(train_dataset, NUM_EPOCS, validation_data=val, callbacks=[tensorboard_callback])

# fig = plt.figure()
# plt.plot(history.history['loss'], color='teal', label='loss')
# plt.plot(history.history['val_loss'], color='orange', label='val_loss')
# fig.suptitle('Loss', fontsize=20)
# plt.legend(loc='upper left')
# plt.show()