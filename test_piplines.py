import os
import unittest
import re

class TestFileNaming(unittest.TestCase):
    
    def setUp(self):
        # Setup: This method is called before each test case
        self.directory = 'test_directory'  # specify your test directory
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        
        # Create some test files with format name_iterator
        self.name = 'file'
        for i in range(5):  # You can change the number of test files
            with open(f"{self.directory}/{self.name}_{i}", 'w') as f:
                f.write(f"Test content for {self.name}_{i}")
    
    def tearDown(self):
        # Teardown: Clean up after each test case
        for file_name in os.listdir(self.directory):
            file_path = os.path.join(self.directory, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(self.directory)

    def test_file_format(self):
        # Check if files in the directory follow the {name}_{iterator} format
        pattern = re.compile(r'^[a-zA-Z0-9]+_\d+$')  # Matches {name}_{iterator} format
        for file_name in os.listdir(self.directory):
            if os.path.isfile(os.path.join(self.directory, file_name)):
                self.assertTrue(pattern.match(file_name), f"File {file_name} does not match the required format")
    
    def test_files_exist(self):
        # Check if the files are created correctly
        for i in range(5):
            file_name = f"{self.name}_{i}"
            self.assertTrue(os.path.exists(os.path.join(self.directory, file_name)), f"{file_name} does not exist")
    
if __name__ == '__main__':
    _ = unittest.main()