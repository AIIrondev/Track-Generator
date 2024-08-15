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

        # Load the image
        self.image_path = "Data/images/trackgerator.png"
        self.image = self.load_image(self.image_path)

        if self.image:
            # Create a canvas for drawing
            self.canvas = tk.Canvas(root, width=self.image.width(), height=self.image.height())
            self.canvas.pack()

            # Display the image on the canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)

            # Bind mouse events to the canvas
            self.canvas.bind("<Button-1>", self.start_draw)
            self.canvas.bind("<B1-Motion>", self.draw)
            self.canvas.bind("<ButtonRelease-1>", self.end_draw)

            self.line = None
        else:
            print("Failed to load image. Exiting.")
            self.root.destroy()
        
        # Create a canvas for drawing
        self.canvas = tk.Canvas(root, width=self.image.width(), height=self.image.height())
        self.canvas.pack()
        
        # Display the image on the canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)

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
        self.line_new = self.canvas.create_line(60,40,60,50, fill="black")
        self.quadrat = self.canvas.create_rectangle(50, 50, 100, 100, fill="red")
        self.line = self.canvas.create_line(event.x, event.y, event.x, event.y, fill="black")

    def draw(self, event):
        if self.line:
            coords = self.canvas.coords(self.line)
            self.canvas.coords(self.line, coords[0], coords[1], event.x, event.y)

    def end_draw(self, event):
        self.line = None


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()