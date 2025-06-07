from tkinter import *
from PIL import Image, ImageTk
import numpy as np

def main():
    params = input("Enter parameters: ")
    generate_test_image(*params.split())
    print("Complete!")

def test_image():
    line = np.linspace(0, 255, 100, True, False, np.uint8)
    array = np.tile(line, (100, 1))
    image = Image.fromarray(array, 'L')
    print(isinstance(image, Image.Image))
    image.save("/home/filip/workspace/boot.dev/sound_gradient_generator/content/image.png", quality=100, subsampling=0)

def generate_test_image(*args):
    if len(args) != 4:
        raise ValueError("Four parameters required")
    width = int(args[0])
    height = int(args[1])
    start = (float(args[2]) / 100.) * pow(2, 8)
    stop = (float(args[3]) / 100.) * pow(2, 8) - 1
    line = np.linspace(start, stop, width, True, False, np.uint8)
    array = np.tile(line, (height, 1))
    image = Image.fromarray(array, "L")
    image.save("/home/filip/workspace/boot.dev/sound_gradient_generator/content/test_image.png")
    display_image(width, height, image)

def display_image(width, height, image):
    win = Tk()
    image_res = str(f"{width}x{height}")
    win.geometry(image_res)
    tk_image = ImageTk.PhotoImage(image)
    image_label = Label(win, image=tk_image)
    image_label.pack()
    win.mainloop()

main()