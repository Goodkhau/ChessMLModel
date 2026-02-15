from abc import ABC, abstractmethod
import tensorflow as tf

class Functional_API_Interface(ABC):
    @abstractmethod
    def define_model(self) -> tf.keras.Model[tf.Tensor, tf.Tensor]:
        pass