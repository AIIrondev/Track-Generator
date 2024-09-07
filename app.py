import json
import customtkinter as ctk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk, UnidentifiedImageError
import os
from mod_save import Save as save
import tkinter as tk
import math
import ctypes
import platform
import sys
import requests
import zipfile
import shutil

with open('Data/config/trackgenerator.config.json', 'r') as f:
    config = json.load(f)

LOCAL_VERSION_FILE = config['version']
UPDATE_FOLDER = 'update_files/'
API_URL = 'https://api.github.com/repos/AIIrondev/Track-Generator/releases/latest'
DOWNLOAD_PATH = 'Trackgenerator.zip'

record_active = False
module_active = False
image_path = config["image_path"]
logo_path = config["logo_path"]
file_path_save = config["save_path"]
__version__ = config["version"]
button_name = config["button_names"]

points = {}
last_point = [718, 495]

class App:
    global record_active
    def get_windows_version(self):
        if platform.system() == "Windows":
            release = platform.release()
            print(f"Windows version: {release}")
            if release == "10":
                return "1200x700"
            elif release == "11":
                return "1200x700"
            else:
                return "1200x700"
        else:
            return "1200x700"

    def __init__(self):
        self.last_point = [718, 495]
        self.orientation = 90
        self.root = ctk.CTk()
        self.root.title("Trackgerator")
        self.root.geometry(self.get_windows_version())
        self.root.resizable(False, False)
        self.root.iconbitmap(logo_path)
        self.trackgerator()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<KeyPress>", self.record_api)
        self.root.mainloop()

    #def display_coor(self, input_new):
    #    print(input_new)

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
            filetypes=[("Trackgenerator", "*.tg")]
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
        if record_active:
            pass
        else:
            record_active = True

    def stop():
        global record_active
        record_active = False

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
        self.app.title("Path Display")
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
        tk.Button(self.app, text="Update", command=Update).pack()


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

class Update:
    def get_local_version(self):
        try:
            return LOCAL_VERSION_FILE
        except FileNotFoundError:
            return "0.0.0"

    def get_latest_release(self):
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(f"Response content: {response.content}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        return None

    def check_for_update(self):
        local_version = self.get_local_version()
        latest_release = self.get_latest_release()

        if latest_release:
            latest_version = latest_release['tag_name']
            print(f"Local version: {local_version}, Latest version: {latest_version}")

            if latest_version > local_version:
                print(f"New version available: {latest_version}")
                return latest_release
            else:
                print("You are already on the latest version.")
                return None
        else:
            print("No update information found.")
            return None

    def download_update(self, asset_url):
        print(f"Downloading update from: {asset_url}")
        response = requests.get(asset_url, stream=True)

        if response.status_code == 200:
            print("Update is getting downloaded...")
            with open(DOWNLOAD_PATH, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            print("Update downloaded.")
            return True
        else:
            print(f"Failed to download update: {response.status_code}")
            return False

    def apply_update(self):
        print("Applying update...")
        try:
            with zipfile.ZipFile(DOWNLOAD_PATH, 'r') as zip_ref:
                zip_ref.extractall(UPDATE_FOLDER)
            for root, dirs, files in os.walk(UPDATE_FOLDER):
                for file in files:
                    full_path = os.path.join(root, file)
                    target_path = os.path.join(os.getcwd(), file)
                    shutil.move(full_path, target_path)
            print("Update applied successfully.")
            os.remove(DOWNLOAD_PATH)
            shutil.rmtree(UPDATE_FOLDER)
            return True
        except Exception as e:
            print(f"Failed to apply update: {e}")
            return False

    def restart_application(self):
        print("Restarting application...")
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def __init__(self):
        latest_release = self.check_for_update()

        if latest_release:
            for asset in latest_release['assets']:
                if asset['name'] == 'Trackgenerator.zip':
                    asset_url = asset['browser_download_url']
                    if self.download_update(asset_url):
                        if self.apply_update():
                            print("Update complete. Restarting now...")
                            self.restart_application()
                    break
            else:
                print("Update.zip file not found in the release assets.")
        else:
            print("No updates to apply.")



if __name__ == '__main__':
    record.initialise()
    App()