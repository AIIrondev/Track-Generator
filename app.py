import json
import customtkinter as ctk
from PIL import Image, ImageTk, UnidentifiedImageError

# Load the configuration file
with open('Data/config/trackgenerator.config.json', 'r') as f:
    config = json.load(f)

image_path = config["image_path"]
logo_path = config["logo_path"]
__version__ = config["version"]

class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Trackgerator")
        self.root.geometry("1000x630")
        self.root.resizable(False, False)
        self.root.iconbitmap(logo_path)
        self.trackgerator()
        self.root.mainloop()

    def trackgerator(self):
        print(f"Image path: {image_path}")
        ctk.CTkLabel(self.root, text=f"Trackgerator v{__version__}").grid(row=2, column=0, columnspan=2, padx=10, pady=10)

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
            match button_number:
                case 1:
                    print(button_pressed[1])
        
        button_name = ["Record", "Play", "Stop", "Pause", "Rewind", "Save", "Load", "New", "Compile", "Settings", "Help"]

        for i in range(5):
            button = ctk.CTkButton(button_frame_1, text=button_name[i], command=lambda i=i: button_callback(i+1))
            button.pack(padx=10, pady=5)

        for i in range(6):
            button = ctk.CTkButton(button_frame_2, text=button_name[i+5], command=lambda i=i: button_callback(i+5+1))
            button.pack(side="left", padx=10, pady=5)


class Menu_right:
    def record():
        print("Record button clicked")
        
    def play():
        print("Play button clicked")
    
    def stop():
        print("Stop button clicked")
    
    def pause():
        print("Pause button clicked")
        
    def rewind():
        print("Rewind button clicked")
        
class Menu_down:
    def save():
        print("Save button clicked")
        
    def load():
        print("Load button clicked")
    
    def new():
        print("New button clicked")
    
    def compile():
        print("Compile button clicked")
    
    def settings():
        print("Settings button clicked")
        
    def help():
        print("Help button clicked")
    
    
    

if __name__ == '__main__':
    App()