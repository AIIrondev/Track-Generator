import customtkinter as ctk
import json
import os
import sys

with open("Data/config/trackgenerator.config", "r") as f:
    config = json.load(f)
    image_path = config["image_path"]
    __version__ = config["version"]

class app:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Trackgerator")
        self.root.geometry("800x600")
        self.trackgerator()
        self.root.mainloop()

    def trackgerator(self):
        # Load and display the image
        image = ctk.CTkImage(file="path/to/your/image.png")
        image_label = ctk.CTkLabel(self.root, image=image)
        image_label.grid(row=0, column=0, rowspan=5, padx=10, pady=10)

        # Create and place four buttons to the right of the image
        for i in range(4):
            button = ctk.CTkButton(self.root, text=f"Button {i+1}")
            button.grid(row=i, column=1, padx=10, pady=5)

        # Create and place five buttons under the image
        for i in range(5):
            button = ctk.CTkButton(self.root, text=f"Button {i+5+1}")
            button.grid(row=5, column=i, padx=10, pady=5)

    
    
if __name__ == '__main__':
    app()