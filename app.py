import json
import customtkinter as ctk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk, UnidentifiedImageError
import os
import webbrowser
from mod_save import Save as save
import tkinter as tk
import math

with open('Data/config/trackgenerator.config.json', 'r') as f:
    config = json.load(f)

record_active = False
module_active = False
image_path = config["image_path"]
logo_path = config["logo_path"]
file_path_save = config["save_path"]
_version__ = config["version"]
button_name = config["button_names"]

points = {}
last_point = [718, 495]

class App:
    global record_active
    def __init__(self):
        self.last_point = [718, 495]
        self.orientation = 90
        self.root = ctk.CTk()
        self.root.title("Trackgerator")
        self.root.geometry("820x470")
        self.root.resizable(False, False)
        self.root.iconbitmap(logo_path)
        self.trackgerator()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<KeyPress>", self.record_api)
        self.root.bind("<Button-1>", self.display_coor)
        self.root.mainloop()

    def display_coor(self, input_new):
        print(input_new)

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

        self.canvas.create_oval(700, 490, 730, 500, fill="red", tags="point")

        def button_callback(button_number):
            global record_active
            match button_number:
                case 1:
                    if record_active:
                        Menu_right.stop()
                    else:
                        Menu_right.record()
                case 2:
                    Menu_right.play()
                case 3:
                    Menu_right.module()
                case 4:
                    record.split()
                case 5:
                    Menu_down.save()
                case 6:
                    self.load()
                case 7:
                    self.clear_canvas()
                case 8:
                    settings()
                case 9:
                    Menu_down.help()
                case _:
                    print("Invalid button number")

        for i in range(4):
            button = ctk.CTkButton(button_frame_1, text=button_name[i], command=lambda i=i: button_callback(i+1))
            button.pack(padx=10, pady=5)

        for i in range(5):
            button = ctk.CTkButton(button_frame_2, text=button_name[i+4], command=lambda i=i: button_callback(i+4+1))
            button.pack(side="left", padx=10, pady=5)

    def record_api(self, record_input):
        global module_active
        global record_active
        if record_active:
            match record_input.char:
                case "w":
                    record.up()
                    self.drive_forward(40)
                case "s":
                    record.down()
                    self.drive_backward(40)
                case "a":
                    record.left()
                    self.rotate(90)
                case "d":
                    record.right()
                    self.rotate(-90)
                case "q":
                    record.left_half()
                    self.rotate(15)
                case "e":
                    record.right_half()
                    self.rotate(-15)
                case "x":
                    record.split()
                    self.canvas.create_rectangle(self.last_point[0]-5, self.last_point[1]-5, self.last_point[0]+5, self.last_point[1]+5, width=2, outline="blue")
                case _:
                    if module_active:
                        match record_input.char:
                            case "1":
                                record.module._1()
                                self.canvas.create_rectangle(self.last_point[0]-5, self.last_point[1]-5, self.last_point[0]+5, self.last_point[1]+5, width=2, outline="green")
                            case "2":
                                record.module._2()
                                self.canvas.create_rectangle(self.last_point[0]-5, self.last_point[1]-5, self.last_point[0]+5, self.last_point[1]+5, width=2, outline="green")
                            case "3":
                                record.module._3()
                                self.canvas.create_rectangle(self.last_point[0]-5, self.last_point[1]-5, self.last_point[0]+5, self.last_point[1]+5, width=2, outline="green")
                            case "4":
                                record.module._4()
                                self.canvas.create_rectangle(self.last_point[0]-5, self.last_point[1]-5, self.last_point[0]+5, self.last_point[1]+5, width=2, outline="green")
                            case _:
                                pass

    def clear_canvas(self):
        self.canvas.delete("all")
        self.last_point = [717, 495]
        self.orientation = 0
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
        self.canvas.create_oval(700, 490, 730, 500, fill="red", tags="point")

    def drive_forward(self, distance):
        rad = math.radians(self.orientation)
        new_x = self.last_point[0] + distance * math.cos(rad)
        new_y = self.last_point[1] - distance * math.sin(rad)
        self.canvas.create_line(self.last_point[0], self.last_point[1], new_x, new_y, width=2, fill="black")
        self.last_point = [new_x, new_y]

    def drive_backward(self, distance):
        rad = math.radians(self.orientation)
        new_x = self.last_point[0] - distance * math.cos(rad)
        new_y = self.last_point[1] + distance * math.sin(rad)
        self.canvas.create_line(self.last_point[0], self.last_point[1], new_x, new_y, width=2, fill="black")
        self.last_point = [new_x, new_y]

    def rotate(self, angle):
        self.orientation = (self.orientation + angle) % 360

    def load(self):
        path_file = filedialog.askopenfilename(
            initialdir="/",
            title="Select file",
            filetypes=[("Text files", "*.txt")]
        )
        with open(path_file, "r") as f:
            path = f.read()
        for i in path.split("|"):
            print(i)
            match i:
                case "1":
                    record.up()
                    self.drive_forward(50)
                case "2":
                    record.left()
                    self.rotate(90)
                case "3":
                    record.down()
                    self.drive_backward(50)
                case "4":
                    record.right()
                    self.rotate(-90)
                case "5":
                    record.left_half()
                    self.rotate(15)
                case "6":
                    record.right_half()
                    self.rotate(-15)
                case "7":
                    record.split()
                    self.canvas.create_rectangle(self.last_point[0]-5, self.last_point[1]-5, self.last_point[0]+5, self.last_point[1]+5, width=2, outline="blue")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to save?"):
            save()
            self.root.destroy()
            exit(0)
        else:
            self.root.destroy()
            exit(0)

class record:
    global record_active
    def initialise():
        with open(file_path_save, "w") as f:
            f.write("")
    def up():
        with open(file_path_save, "a") as f:
            f.write("1|")
    def down():
        with open(file_path_save, "a") as f:
            f.write("3|")
    def left():
        with open(file_path_save, "a") as f:
            f.write("2|")
    def right():
        with open(file_path_save, "a") as f:
            f.write("4|")
    def left_half():
        with open(file_path_save, "a") as f:
            f.write("5|")
    def right_half():
        with open(file_path_save, "a") as f:
            f.write("6|")
    def split():
        with open(file_path_save, "a") as f:
            f.write("7|")
    class module:
        def _1():
            # +40
            with open(file_path_save, "a") as f:
                f.write("8|")
        def _2():
            # -40
            with open(file_path_save, "a") as f:
                f.write("9|")
        def _3():
            # +120
            with open(file_path_save, "a") as f:
                f.write("10|")
        def _4():
            # -120
            with open(file_path_save, "a") as f:
                f.write("11|")

class Menu_right:
    def record():
        global record_active
        print("Record button clicked")
        if record_active:
            pass
        else:
            record_active = True

    def play():
        Display_path()

    def module():
        global module_active
        if module_active:
            module_active = False
        else:
            module_active = True

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

        with open(file_path_save, "r") as f:
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

class settings:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Settings")
        self.app.geometry("500x500")
        self.app.resizable(False, False)
        self.app.iconbitmap(logo_path)
        self.settings()
        self.app.mainloop()

    def settings(self):
        tk.Label(self.app, text="Settings").pack()
        tk.Button(self.app, text="Update", command=self.update).pack()

    def update(self):
        pass


class Menu_down:
    def save():
        save()

    def help():
        print("Help button clicked")
        if messagebox.askokcancel("Help", "If you click ok youre browser will open the help Website for you."):
            pass
            #webbrowser("https://github.com")
        else:
            pass


if __name__ == '__main__':
    record.initialise()
    App()