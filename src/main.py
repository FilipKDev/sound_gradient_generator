from tkinter import *
from PIL import Image, ImageTk
import numpy as np

class Window:
    def __init__(self, width, height, start = 0, stop = 100):
        self.__root = Tk()
        self.__root.title = "Gradient Generator"

        self._width = int(width)
        self._height = int(height)
        self._start = self._percentage_to_8bit(start)
        self._stop = self._percentage_to_8bit(stop) - 1

        self.__root.geometry(f"{self._width}x{self._height+50}")
        self._im = GradientImage(self._width, self._height, self._start, self._stop, self.__root)
        self._im.generate_image()
        self._create_buttons()

    def run(self):
        self.__root.mainloop()

    def test(self):
        print("Test button pressed")
        print(self._width)
        print(self._height)
        print(self._start)
        print(self._stop)

    def _create_buttons(self):
        self.__roll_left_button = Button(self.__root, text="Flip", command=self._flip_gradient)
        self.__roll_right_button = Button(self.__root, text="TEST", command=self.test)
        self.__roll_left_button.place(x=10, y=self._height+5, width = 80, height = 40)
        self.__roll_right_button.place(x=self._width - 90, y=self._height+5, width = 80, height = 40)

    def _flip_gradient(self):
        self._im.flip_gradient()

    def _percentage_to_8bit(self, input):
        return (float(input) / 100.) * pow(2, 8)

class GradientImage:
    def __init__(self, width, height, start, stop, win_root = None):
        self.line = np.linspace(start, stop, width, True, False, np.uint8)
        self.win_root = win_root
        self._height = height
        self.image_label = None

    def generate_image(self):
        self._image_array = np.tile(self.line, (self._height, 1))
        self._image = Image.fromarray(self._image_array, "L")
        self._image.save("/home/filip/workspace/boot.dev/sound_gradient_generator/content/gradient_image.png")
        self._display_image(self._image)

    def _display_image(self, image):
        if self.image_label:
            self.image_label.pack_forget()
        self._image_tk = ImageTk.PhotoImage(image)
        self.image_label = Label(self.win_root, image=self._image_tk)
        self.image_label.pack()
    
    def flip_gradient(self):
        self.line = self.line[::-1]
        self.generate_image()
        

def test_image():
    line = np.linspace(0, 255, 100, True, False, np.uint8)
    array = np.tile(line, (100, 1))
    image = Image.fromarray(array, 'L')
    print(isinstance(image, Image.Image))
    image.save("/home/filip/workspace/boot.dev/sound_gradient_generator/content/image.png", quality=100, subsampling=0)

def generate_test_image(*args):
    if len(args) < 2:
        raise ValueError("Minimum arguments required: Width, Height")
    win = Window(args[0], args[1], args[2], args[3])
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