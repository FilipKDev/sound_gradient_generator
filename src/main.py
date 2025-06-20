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
        self._v1 = DoubleVar()
        #self.canvas = Canvas(self.__root, width = width, height = 45)
        #self.canvas.place(x=0, y=self._height+5)
        self._create_buttons_testing()
        #self._create_slider_testing()

    def run(self):
        self.__root.mainloop()

    def test(self):
        print("Test button pressed")
        print(self._width)
        print(self._height)
        print(self._start)
        print(self._stop)

    def _display_data(self):
        print(self._im.line)

    def _create_buttons(self):
        self.__roll_left_button = Button(self.__root, text="Move Left", command=self._im.roll_left, repeatinterval=10, repeatdelay=250)
        self.__flip_button = Button(self.__root, text="Flip", command=self._im.flip_gradient)
        self.__roll_right_button = Button(self.__root, text="Move Right", command=self._im.roll_right, repeatinterval=10, repeatdelay=250)
        self.__roll_left_button.place(x=10, y=self._height+5, width=80, height=40)
        self.__flip_button.place(x=self._width / 2 - 40, y= self._height+5, width=80, height=40)
        self.__roll_right_button.place(x=self._width - 90, y=self._height+5, width=80, height=40)

    def _create_buttons_testing(self):
        self.__roll_left_button = Button(self.__root, text="", command=self._im.roll_left, repeatinterval=10, repeatdelay=250)
        self.__flip_button = Button(self.__root, text="", command=self._display_data)
        self.__roll_right_button = Button(self.__root, text="", command=self._im.roll_right, repeatinterval=10, repeatdelay=250)
        self.__roll_left_button.place(x=10, y=self._height+5, width=10, height=40)
        self.__flip_button.place(x=self._width / 2 - 5, y= self._height+5, width=10, height=40)
        self.__roll_right_button.place(x=self._width - 20, y=self._height+5, width=10, height=40)

    def _create_slider_testing(self):
        self.__test_slider = Scale(self.__root, variable=self._v1, from_=0, to=1, orient = HORIZONTAL, digits=3, resolution=0.01, sliderlength=10, showvalue=0)
        self.__test_slider.place(x=0, y=self._height+5, width=self._width, height=40)

    def _percentage_to_8bit(self, input):
        return (float(input) / 100.) * pow(2, 8)

class GradientImage:
    def __init__(self, width, height, start, stop, win_root = None):
        self.line = np.linspace(start, stop, width, True, False, np.uint8)
        self.win_root = win_root
        self._height = height
        self._width = width
        self.image_label = None
        self._roll_line = self.line[::-1]

    def generate_image(self):
        self._image_array = np.tile(self.line, (self._height, 1))
        self._image = Image.fromarray(self._image_array, "L")
        self._image.save("/home/filip/workspace/boot.dev/sound_gradient_generator/content/gradient_image.png")
        self._image_tk = ImageTk.PhotoImage(self._image)
        if not self.image_label:
            self._display_image(self._image_tk)
        else:
            self._update_image(self._image_tk)

    def _display_image(self, image):
        if self.image_label:
            self.image_label.pack_forget()
        self.image_label = Label(self.win_root, image=image)
        self.image_label.pack()

    def _update_image(self, image):
        self.image_label.config(image=image)
    
    def flip_gradient(self):
        self._roll_line = self._roll_line[::-1]
        self.line = self.line[::-1]
        self.generate_image()

    def roll_left(self):
        self._increment = int(self._width / 10)
        self._chunk = self._roll_line[:self._increment]
        self._roll_line = self._roll_line[self._increment:]
        self.line = np.append(self.line, self._chunk)
        self._roll_line = np.append(self._roll_line, self.line[:self._increment])
        self.line = self.line[self._increment:]
        self.generate_image()

    def roll_right(self):
        self._increment = int(self._width / 10)
        self._chunk = self._roll_line[-self._increment:]
        self._roll_line = self._roll_line[:-self._increment]
        self.line = np.append(self._chunk, self.line)
        self._roll_line = np.append(self.line[-self._increment:], self._roll_line)
        self.line = self.line[:-self._increment]
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