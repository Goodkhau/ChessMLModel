from abc import ABC, abstractmethod

class Pipeline_Interface(ABC):
    @abstractmethod
    def train_model(self, model) -> None:
        pass