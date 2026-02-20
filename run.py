import tensorflow as tf
import sys
from data.DataPipeline import TFRecords, Pipeline_Interface
from base.model_V1_0.model_V1 import model_V1
from prompter import get_input


if __name__ == "__main__":
    selection: int = -1
    while (selection):
        pipeline: None | Pipeline_Interface = None
        model = None
        match (selection):
            case 1:
                pipeline = TFRecords()
                pipeline.populate_training_data(default_size=10000, default_games=10000)
            case 2:
                model = model_V1().model
                model.summary()
            case 3:
                if model is None:
                    print("Model not selected.\n")
                    continue

                if pipeline is None:
                    print("Pipeline not selected.\n")  # pyright: ignore[reportUnreachable]
                    continue

                pipeline.train_model(model)
            case _:
                print("Choose a valid selection")
        selection = get_input(lower=0, upper=3, prompt=f"Select an option\n1: Load and Partition Dataset.\n2: Select Model.\n3: Train and Output Model.\n")

    print("Exiting.\n")

else:
    print("File exist only as an entry point.\nExiting.\n")
    sys.exit()