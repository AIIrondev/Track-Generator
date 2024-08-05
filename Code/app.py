import customtkinter as ctk

def main():
    root = ctk.Tk()
    root.title("Trackgerator")
    root.geometry("800x600")
    trackgerator()
    root.mainloop()

def trackgerator():
    ctk.PhotoImage(file="images/trackgerator.png")
    ctk.CtkLabel(text="Trackgerator", font=("Arial", 24)).pack()
    
    
if __name__ == '__main__':
    main()