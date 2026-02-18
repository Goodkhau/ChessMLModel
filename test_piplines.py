import os
import unittest
from os import listdir
from os.path import isfile, join
from pathlib import Path
from data.DataPipeline import Pipeline_Interface, TFRecords

class test_populate_pipeline(unittest.TestCase):
    def test_populate(self):
        pipeline: Pipeline_Interface = TFRecords()
        pipeline.populate_training_data(default_size=10, default_games=100)

        name = pipeline.name
        directory: str = f"{Path.cwd()}/data/training_data/"
        self.assertTrue(expr=any([file for file in listdir(path=directory) if (file[:-5] == name)]))

        for file in listdir(directory):
            if file[:-5] != name:
                continue
            print("Removing: " + directory + file)
            os.remove(path=directory+file)
    
if __name__ == '__main__':
    _ = unittest.main()