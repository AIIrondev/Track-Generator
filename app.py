import json
import customtkinter as ctk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk, UnidentifiedImageError

# Load the configuration file
with open('Data/config/trackgenerator.config.json', 'r') as f:
    config = json.load(f)

image_path = config["image_path"]
logo_path = config["logo_path"]
__version__ = config["version"]
button_name = config["button_names"]

class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Trackgerator")
        self.root.geometry("1000x630")
        self.root.resizable(False, False)
        self.root.iconbitmap(logo_path)
        self.trackgerator()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def trackgerator(self):
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
                    Menu_right.record()
                case 2:
                    Menu_right.play()
                case 3:
                    Menu_right.stop()
                case 4:
                    Menu_right.pause()
                case 5:
                    Menu_right.rewind()
                case 6:
                    Menu_down.save()
                case 7:
                    Menu_down.load()
                case 8:
                    Menu_down.new()
                case 9:
                    Menu_down.compile()
                case 10:
                    Menu_down.settings()
                case 11:
                    Menu_down.help()
                case _:
                    print("Invalid button number")

        for i in range(5):
            button = ctk.CTkButton(button_frame_1, text=button_name[i], command=lambda i=i: button_callback(i+1))
            button.pack(padx=10, pady=5)

        for i in range(6):
            button = ctk.CTkButton(button_frame_2, text=button_name[i+5], command=lambda i=i: button_callback(i+5+1))
            button.pack(side="left", padx=10, pady=5)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            exit(0)


class recording:
    def __init__(self):
        pass

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