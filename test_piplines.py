import os
import unittest
from pathlib import Path
from data.DataPipeline import Pipeline_Interface, TFRecords

class test_populate_pipeline(unittest.TestCase):
    ## Need to run in debug mode, python GIL is giving error not relevent to test
    def test_populate(self):
        pipeline: Pipeline_Interface = TFRecords()
        pipeline.populate_training_data(default_size=10, default_games=100)

        name = pipeline.name
        directory: str = f"{Path.cwd()}/data/training_data/{name}/"
        self.assertTrue(expr=any([file for file in os.listdir(path=directory) if (file[:-5] == name)]))

        for file in os.listdir(directory):
            if file[:-5] != name:
                continue
            print("Removing: " + directory + file)
            os.remove(path=directory+file)
        os.rmdir(directory)
    
if __name__ == '__main__':
    _ = unittest.main()