import os
import shutil
import customtkinter as ctk
from tkinter import messagebox


class app:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Test")
        self.root.geometry("1000x470")
        self.root.resizable(False, False)
        self.record_app()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<KeyPress>", self.record_api)
        self.root.mainloop()
    def record_api(self, record_input):
        match record_input.char:
            case "w":
                record.up()
            case "a":
                record.left()
            case "s":
                record.down()
            case "d":
                record.right()
            case "":
                self.on_closing()
            case "":
                self.save()
    def record_app(self):
        ctk.CTkButton(self.root, text="Start recording")
        ctk.CTkLabel(self.root, text="this will be valid")
    def save(self):
        pass
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            exit(0)

class record:
    def initialise(filepath):
        if os.path.exists(filepath):
            os.remove(filepath)
        else:
            with open(filepath, "w") as f:
                f.write("")
    def up():
        with open(filepath, "a") as f:
            f.write("1")
    def down():
        with open(filepath, "a") as f:
            f.write("2")
    def left():
        with open(filepath, "a") as f:
            f.write("3")
    def right():
        with open(filepath, "a") as f:
            f.write("4")

if __name__ == "__main__":
    app()