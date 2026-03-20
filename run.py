import sys
from data.Pipeline_Interface import Pipeline_Interface
from data.CycleData import Cycle_Data
from base.Little_Blue.model_V1 import model_V1
from prompter import get_input


if __name__ == "__main__":
    selection: int = -1
    while (selection):
        pipeline: Pipeline_Interface
        match (selection):
            case 1:
                pipeline = Cycle_Data()
            case 2:
                model = model_V1().model
                model.summary()
            case 3:
                pipeline.train_model(model)  # pyright: ignore[reportUnreachable]
            case _:
                print("Choose a valid selection")
        selection = get_input(lower=0, upper=3, prompt=f"Select an option\n1: Load and Partition Dataset.\n2: Select Model.\n3: Train and Output Model.\n")

    print("Exiting.\n")

else:
    print("File exist only as an entry point.\nExiting.\n")
    sys.exit()