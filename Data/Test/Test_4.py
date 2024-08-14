import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, UnidentifiedImageError

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing App")

        # Create a frame for the image
        self.image_frame = ttk.Frame(root)
        self.image_frame.pack()

        # Load and display the image
        self.load_image("Data/images/trackgenerator.png")

        # Create a canvas for drawing
        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.canvas.pack()

        # Bind mouse events to the canvas
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

        self.line = None

    def load_image(self, image_path):
        try:
            image = Image.open(image_path)
            resized_image = image.resize((250, 250))
            photo_image = ImageTk.PhotoImage(resized_image)
        except FileNotFoundError:
            print(f"Error: File not found at {image_path}")
            return
        except UnidentifiedImageError:
            print(f"Error: Cannot identify image file at {image_path}")
            return

        image_label = ttk.Label(self.image_frame, image=photo_image)
        image_label.image = photo_image
        image_label.pack()

    def start_draw(self, event):
        self.line = self.canvas.create_line(event.x, event.y, event.x, event.y, fill="black")

    def draw(self, event):
        if self.line:
            coords = self.canvas.coords(self.line)
            self.canvas.coords(self.line, coords[0], coords[1], event.x, event.y)

    def end_draw(self, event):
        self.line = None

    def export_canvas(self):
        # Get the canvas coordinates
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()

        # Capture the canvas content
        ImageGrab.grab().crop((x, y, x1, y1)).save("canvas_export.png")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()