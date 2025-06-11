from tkinter import *
from PIL import Image, ImageTk
import numpy as np

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title = "Gradient Generator"
        self.__root.geometry(f"{width}x{height+50}")
        self.__test_button = Button(self.__root, text="TEST", command=self.test)
        self.__test_button.place(x=10, y=height+5, width = 50, height = 40)

    def display_image(self, image):
        self.__image = ImageTk.PhotoImage(image)
        self.__image_label = Label(self.__root, image=self.__image)
        self.__image_label.pack(side="top")

    def run(self):
        self.__root.mainloop()

    def test(self):
        print("Test button pressed")

def test_image():
    line = np.linspace(0, 255, 100, True, False, np.uint8)
    array = np.tile(line, (100, 1))
    image = Image.fromarray(array, 'L')
    print(isinstance(image, Image.Image))
    image.save("/home/filip/workspace/boot.dev/sound_gradient_generator/content/image.png", quality=100, subsampling=0)

def generate_test_image(*args):
    if len(args) != 5:
        raise ValueError("Five parameters required")
    width = int(args[0])
    height = int(args[1])
    start = (float(args[2]) / 100.) * pow(2, 8)
    stop = (float(args[3]) / 100.) * pow(2, 8) - 1
    
    line = None
    if args[4] == '2':
        line = two_point_gradient(start, stop, width)
    elif args[4] == '3':
        line = three_point_gradient(start, stop, width)
    else:
        raise Exception("Not supported")
    
    array = np.tile(line, (height, 1))
    image = Image.fromarray(array, "L")
    image.save("/home/filip/workspace/boot.dev/sound_gradient_generator/content/test_image.png")
    win = Window(width, height)
    win.display_image(image)
    win.run()

def two_point_gradient(start, stop, width):
    return np.linspace(start, stop, width, True, False, np.uint8)

def three_point_gradient(start, stop, width):
    midpoint = int(width / 2)
    line1 = np.linspace(start, stop, midpoint, True, False, np.uint8)
    line2 = np.linspace(stop - 1, start, midpoint, True, False, np.uint8)
    return np.concatenate((line1, line2))

def main():
    params = input("Enter parameters: ")
    generate_test_image(*params.split())
    print("Complete!")

main()