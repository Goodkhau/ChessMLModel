import tensorflow as tf
from tensorflow import Tensor
from base.Model_Interface import Functional_API_Interface

MODEL_NAME = 'Little Blue'
LOGDIR: str = f"../log/{MODEL_NAME}"
BATCH_SIZE = 128
NUM_EPOCS = 10
NUM_CLASSES = 386

class model_V1(Functional_API_Interface):
    def __init__(self) -> None:
        self.model= self.define_model()
    
    def define_model(self):
        input: Tensor = tf.keras.Input(shape=(8, 8, 8))
        flat: Tensor = tf.keras.layers.Flatten(shape=(512,))(input)
        first_dense: Tensor = tf.keras.layers.Dense(units=1024)(inputs=flat)
        second_dense: Tensor = tf.keras.layers.Dense(units=1024)(inputs=first_dense)
        third_dense: Tensor = tf.keras.layers.Dense(units=768)(inputs=second_dense)
        fourth_dense: Tensor = tf.keras.layers.Dense(units=512)(inputs=third_dense)
        outputs: Tensor = tf.keras.layers.Dense(units=NUM_CLASSES, activation='sigmoid')(inputs=fourth_dense)
        model: tf.keras.Model[Tensor, Tensor] = tf.keras.Model(inputs=input, outputs=outputs, name=MODEL_NAME)
        model.compile(optimizer='adam', loss=tf.losses.SparseCategoricalCrossentropy(), metrics=['accuracy'])
        return model