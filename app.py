import json
import customtkinter as ctk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk, UnidentifiedImageError
import os
import webbrowser
from mod_save import Save as save
import tkinter as tk

# Load the configuration file
with open('Data/config/trackgenerator.config.json', 'r') as f:
    config = json.load(f)

record_active = False
image_path = config["image_path"]
logo_path = config["logo_path"]
__version__ = config["version"]
button_name = config["button_names"]

last_point = [717, 495]
points = {}

class App:
    global record_active
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Trackgerator")
        self.root.geometry("1000x470")
        self.root.resizable(False, False)
        self.root.iconbitmap(logo_path)
        self.trackgerator()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<KeyPress>", self.record_api)
        self.root.bind("<Button-1>", self.printcoords)
        self.root.mainloop()

    def printcoords(self, event):
        print(event.x, event.y)

    def trackgerator(self):

        ctk.CTkLabel(self.root, text=f"Trackgerator v{__version__}", text_color="blue").grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        image_frame = ctk.CTkFrame(self.root)
        button_frame_1 = ctk.CTkFrame(self.root)
        button_frame_2 = ctk.CTkFrame(self.root)

        image_frame.grid(row=0, column=0, padx=10, pady=10)
        button_frame_1.grid(row=0, column=1, padx=10, pady=10)
        button_frame_2.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.canvas = ctk.CTkCanvas(image_frame, width=800, height=500, bg="white")
        self.canvas.pack()
        try:
            image = Image.open(image_path)
            resized_image = image.resize((800, 500))
            self.photo_image = ImageTk.PhotoImage(resized_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image, tags="background")
        except FileNotFoundError:
            print(f"Error: File not found at {image_path}")
            return
        except UnidentifiedImageError:
            print(f"Error: Cannot identify image file at {image_path}")
            return

        self.photo_image = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image, tags="background")

        self.canvas.create_oval(700, 490, 730, 500, fill="red", tags="point")

        def button_callback(button_number):
            match button_number:
                case 1:
                    if record_active:
                        Menu_right.stop()
                    else:
                        Menu_right.record()
                case 2:
                    Menu_right.play()
                case 3:
                    Menu_right.pause()
                case 4:
                    Menu_right.rewind()
                case 5:
                    Menu_right.split()
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

    def record_api(self, record_input):
        if record_active:
            self.draw(record_input.char)
            match record_input.char:
                case "w":
                    record.up()
                case "a":
                    record.left()
                case "s":
                    record.down()
                case "d":
                    record.right()
                case "q":
                    record.left_half()
                case "e":
                    record.right_half()
                case "x":
                    record.split()
                case "":
                    self.on_closing()
                case "":
                    self.save()

    def draw(self, record_input):
        match record_input:
            case "w":
                self.canvas.create_line(last_point[0], last_point[1], last_point[0], last_point[1]-10, width=2, fill="black")
                last_point[1] -= 50
            case "a":
                self.canvas.create_line(last_point[0], last_point[1], last_point[0]-10, last_point[1], width=2, fill="black")
                last_point[0] -= 50
            case "s":
                self.canvas.create_line(last_point[0], last_point[1], last_point[0], last_point[1]+10, width=2, fill="black")
                last_point[1] += 50
            case "d":
                self.canvas.create_line(last_point[0], last_point[1], last_point[0]+10, last_point[1], width=2, fill="black")
                last_point[0] += 50
            case "q":
                self.canvas.create_line(last_point[0], last_point[1], last_point[0]-5, last_point[1], width=2, fill="black")
                last_point[0] -= 20
                last_point[1] -= 20
            case "e":
                self.canvas.create_line(last_point[0], last_point[1], last_point[0]+5, last_point[1], width=2, fill="black")
                last_point[0] += 20
                last_point[1] -= 20
            case "x":
                self.canvas.create_rectangle(last_point[0]-5, last_point[1]-5, last_point[0]+5, last_point[1]+5, width=2, outline="black")
            case _:
                pass

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            exit(0)

class record:
    global record_active
    def initialise():
        if os.path.exists("Data/config/path.txt"):
            os.remove("Data/config/path.txt")
        else:
            with open("Data/config/path.txt", "w") as f:
                f.write("")
    def up():
        with open("Data/config/path.txt", "a") as f:
            f.write("1|")
    def down():
        with open("Data/config/path.txt", "a") as f:
            f.write("3|")
    def left():
        with open("Data/config/path.txt", "a") as f:
            f.write("2|")
    def right():
        with open("Data/config/path.txt", "a") as f:
            f.write("4|")
    def left_half():
        with open("Data/config/path.txt", "a") as f:
            f.write("5|")
    def right_half():
        with open("Data/config/path.txt", "a") as f:
            f.write("6|")
    def split():
        with open("Data/config/path.txt", "a") as f:
            f.write("7|")

class Menu_right:
    def record():
        global record_active
        print("Record button clicked")
        if record_active:
            pass
        else:
            record_active = True

    def play():
        print("Play button clicked")

    def stop():
        global record_active
        print("Stop button clicked")
        if record_active:
            record_active = False
        else:
            pass

    def pause():
        global record_active
        print("Pause button clicked")
        if record_active:
            record_active = False
        else:
            pass

    def rewind():
        Display_path()

    def split():
        with open("Data/config/path.txt", "a") as f:
            f.write("5|")

class Display_path:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Path")
        self.app.geometry("500x500")
        self.app.resizable(False, False)
        self.app.iconbitmap(logo_path)
        self.display_path()
        self.app.mainloop()

    def display_path(self):
        self.frame = tk.Frame(self.app)
        self.frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(self.frame)
        scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        with open("Data/config/path.txt", "r") as f:
            path = f.read()

        for i in path.split("|"):
            match i:
                case "1":
                    tk.Label(scrollable_frame, text="Up").pack()
                case "2":
                    tk.Label(scrollable_frame, text="Left").pack()
                case "3":
                    tk.Label(scrollable_frame, text="Down").pack()
                case "4":
                    tk.Label(scrollable_frame, text="Right").pack()
                case "5":
                    tk.Label(scrollable_frame, text="Left Half").pack()
                case "6":
                    tk.Label(scrollable_frame, text="Right Half").pack()
                case "7":
                    tk.Label(scrollable_frame, text="New Section").pack()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.app.destroy()
            exit(0)

class Menu_down:
    def save():
        save()

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
        if messagebox.askokcancel("Help", "If you click ok youre browser will open the help Website for you."):
            pass
            #webbrowser("https://website.github.com")
        else:
            pass


if __name__ == '__main__':
    record.initialise()
    App()