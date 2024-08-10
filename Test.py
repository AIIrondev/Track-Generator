import os

class record:
    def __init__(self):
        # This will be the function that will be used to record the data
        
        pass
    
    def up(self):
        print("Upwards button clicked")
        with open("test.txt", "a") as f:
            f.write("1")
        
    def down(self):
        print("Downwards button clicked")
        with open("test.txt", "a") as f:
            f.write("2")
        
    def left(self):
        print("Leftwards button clicked")
        with open("test.txt", "a") as f:
            f.write("3")
        
    def right(self):
        print("Rightwards button clicked")
        with open("test.txt", "a") as f:
            f.write("4")
            
if __name__ == "__main__":
    Menu_right = record()
    Menu_right.up()
    Menu_right.down()
    Menu_right.left()
    Menu_right.right()
    print("Test completed")