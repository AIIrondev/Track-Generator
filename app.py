import json
import customtkinter as ctk
from PIL import Image, ImageTk, UnidentifiedImageError

# Load the configuration file
with open('Data/config/trackgenerator.config.json', 'r') as f:
    config = json.load(f)

image_path = config["image_path"]
__version__ = config["version"]

class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Trackgerator")
        self.root.geometry("800x600")
        self.trackgerator()
        self.root.mainloop()

    def trackgerator(self):
        print(f"Image path: {image_path}")
        ctk.CTkLabel(self.root, text=f"Trackgerator v{__version__}").grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        image_frame = ctk.CTkFrame(self.root)
        button_frame_1 = ctk.CTkFrame(self.root)
        button_frame_2 = ctk.CTkFrame(self.root)

        image_frame.grid(row=0, column=0, padx=10, pady=10)
        button_frame_1.grid(row=0, column=1, padx=10, pady=10)
        button_frame_2.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        try:
            image = Image.open(image_path)
            resized_image = image.resize((800, 500))
            photo_image = ImageTk.PhotoImage(resized_image)
        except FileNotFoundError:
            print(f"Error: File not found at {image_path}")
            return
        except UnidentifiedImageError:
            print(f"Error: Cannot identify image file at {image_path}")
            return

        image_label = ctk.CTkLabel(image_frame, image=photo_image)
        image_label.image = photo_image
        image_label.pack()

        def button_callback(button_number):
            print(f"Button {button_number} clicked")

        for i in range(4):
            button = ctk.CTkButton(button_frame_1, text=f"Button {i+1}", command=lambda i=i: button_callback(i+1))
            button.pack(padx=10, pady=5)

        for i in range(5):
            button = ctk.CTkButton(button_frame_2, text=f"Button {i+5+1}", command=lambda i=i: button_callback(i+5+1))
            button.pack(side="left", padx=10, pady=5)

if __name__ == '__main__':
    App()