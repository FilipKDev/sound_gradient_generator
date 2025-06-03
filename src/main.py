from PIL import Image
from practice import *
import numpy as np

def main():
    test_image()

def test_image():
    data = NumArray2D_VLin(0, 255, 100, 100)
    array = np.array(data)
    array = array.astype(np.uint8)
    image = Image.fromarray(array, 'L')
    print(isinstance(image, Image.Image))
    image.save("/home/filip/workspace/boot.dev/sound_gradient_generator/content/image.png")

main()