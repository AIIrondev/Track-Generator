import os
import shutil

class save:
    def __init__(self):
        self.filepath = "Data/config/path.txt"
        with open(self.filepath, "r") as f:
            self.content = f.read()