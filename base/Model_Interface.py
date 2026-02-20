from abc import ABC, abstractmethod
from typing import Any
import tensorflow as tf

class Functional_API_Interface(ABC):
    @abstractmethod
    def define_model(self) -> Any:
        pass