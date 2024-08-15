import os
import customtkinter as tk


class App:
    def __init__(self):
        self.root = tk.CTk()
        self.root.title("Test")
        self.root.geometry("1000x470")
        self.draw()
        self.root.mainloop()
    
    def draw(self):
        frame = tk.CTkFrame(self.root)
        frame.grid(row=0, column=0, padx=10, pady=10)
        button = tk.CTkButton(frame, text="Click me", command=self.button_callback)
        button.pack()