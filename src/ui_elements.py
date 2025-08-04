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

        self._ui_area = 250

        #self.__root.geometry(f"{self._width}x{self._height+self._ui_area}")
        self.__root.minsize(self._width, self._height+self._ui_area)
        self.__root.maxsize(self._width, self._height+self._ui_area)
        self.__root.resizable(width=False, height=False)
        self._im = GradientImage(self._width, self._height, self._start, self._stop, self.__root)
        self._im.generate_image()

        self._v1 = DoubleVar()
        
        self.canvas = Canvas(self.__root, width = self._width, height = self._ui_area)
        self.canvas.place(x=0, y=self._height)
        self._slider = Slider(
            self,
            self.canvas,
            x=10, 
            y=5, 
            height=40, 
            length=self._width-20, 
            line_width = 0)

    def get_root(self):
        return self.__root

    def run(self):
        self.__root.mainloop()

    def debug_setup(self):
        #self.canvas.bind("<Button-1>", self._mouse_location)
        self._create_buttons_slider_test()
        #self._create_buttons_testing()
        #self._create_slider_testing()

    def get_endpoint_colors(self):
        return (self._start, self._stop)

    def get_gradient(self):
        return self._im.line
    
    def set_gradient(self, array):
        self._im.line = array
        self._im.generate_image()

    def _display_data(self):
        print(self._im.line)

    def _mouse_location(self, event):
        print(event.x, event.y)

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

class Slider: # Slider widget with multi-cursor support for gradient manipulation
    def __init__(self, win, canvas, **kwargs):
        self.__dict__.update(kwargs)

        self._win = win
        self._canvas = canvas
        self._x = self.__dict__.get('x', 0)
        self._y = self.__dict__.get('y', 0)
        self.length = self.__dict__.get('length', 50)
        self._height = self.__dict__.get('height', 10)

        self._cursor_width = self.__dict__.get('cursor_width', 20)
        self._line_width = self.__dict__.get('line_width', 1)
        
        self._cursors = []
        self._cursor_shades = [0, 255, 0, 255, 0, 255, 0, 255]
        self._create_slider_background()
        #self._create_cursors_test()
        self._create_slider_buttons()

    def _create_slider_background(self):
        if not self._canvas:
            return
        self._canvas.create_rectangle(self._x, self._y, self._x+self.length, self._y+self._height, outline="black", width=self._line_width, fill="#9AAFD0")

    def _create_cursor(self):
        if not self._canvas:
            return   
        self._cursor = GradientCursor(
            self,
            self._canvas, 
            self._x,
            self._y, 
            self._height,
            self._line_width,  
            self._cursor_width)
            
    def _create_cursors_test(self):
        if not self._canvas:
            return
        self._cursor_left = GradientCursor(
            self,
            self._canvas,
            self._x,
            self._y,
            self._height,
            self._line_width,
            self._cursor_width,
            0,
            0
        )
        self._cursor_right = GradientCursor(
            self,
            self._canvas,
            self._x,
            self._y,
            self._height,
            self._line_width,
            self._cursor_width,
            1,
            255
        )
        self._cursors.append(self._cursor_left)
        self._cursors.append(self._cursor_right)
        self._cursor_right.set_x(1)
            
    def update_gradient_test(self, position): # Test method for changing image gradient
        _init_gradient = self._win.get_gradient()
        _true_position = int(len(_init_gradient) * position)
        _new_gradient = np.linspace(self._win.get_endpoint_colors()[0], self._win.get_endpoint_colors()[1], len(_init_gradient)-_true_position, True, False, np.uint8)
        _gradient_padding = np.full((1,_true_position), 0)
        _gradient = np.concatenate((_gradient_padding[0], _new_gradient))
        _gradient = _gradient.astype(np.uint8)
        self._win.set_gradient(_gradient)

    def recalculate_gradient_test_two_cursors(self):
        if len(self._cursors) < 2:
            return
        self._sort_cursors()
        _distance = self._cursors[1].cursor_position - self._cursors[0].cursor_position
        _distance = round(len(self._win.get_gradient())*_distance)
        _new_gradient = np.linspace(self._cursors[0].shade, self._cursors[1].shade, abs(round(_distance)), True, False, np.uint8)
        _left_padding = []
        _right_padding = []
        _left_padding_size = len(self._win.get_gradient())*self._cursors[0].cursor_position
        _right_padding_size = len(self._win.get_gradient())*(1-self._cursors[1].cursor_position)

        if self._cursors[0].cursor_position > 0:
            _left_padding = np.full((1, round(_left_padding_size)), self._cursors[0].shade)
            _left_padding = _left_padding[0]
        if self._cursors[1].cursor_position < 1:
            _right_padding = np.full((1, round(_right_padding_size)), self._cursors[1].shade)
            _right_padding = _right_padding[0]
        _new_gradient = np.concatenate((_left_padding, _new_gradient, _right_padding))
        _new_gradient = _new_gradient.astype(np.uint8)
        self._win.set_gradient(_new_gradient)

    def recalculate_gradient(self):
        if len(self._cursors) < 2:
            return
        self._sort_cursors()
        gradients = []
        for i in range(1, len(self._cursors)):
            distance = self._cursors[i].cursor_position - self._cursors[i-1].cursor_position
            distance = round(len(self._win.get_gradient())*distance)
            gradient = np.linspace(self._cursors[i-1].shade, self._cursors[i].shade, distance, True, False, np.uint8)
            gradients.append(gradient)
        
        left_padding = []
        if self._cursors[0].cursor_position > 0:
            left_padding_size = len(self._win.get_gradient())*self._cursors[0].cursor_position
            left_padding = np.full((1, round(left_padding_size)), self._cursors[0].shade)[0]
        right_padding = []
        if self._cursors[-1].cursor_position < 1:
            right_padding_size = len(self._win.get_gradient())*(1-self._cursors[-1].cursor_position)
            right_padding = np.full((1, round(right_padding_size)), self._cursors[-1].shade)[0]
        if len(left_padding) > 0 and len(right_padding) > 0:
            print(f"Left: {left_padding[0]}")
            print(f"Right: {right_padding[0]}")
        new_gradient = []
        new_gradient = np.append(new_gradient, left_padding)
        for gradient in gradients:
            new_gradient = np.append(new_gradient, gradient)
        new_gradient = np.append(new_gradient, right_padding)
        new_gradient = new_gradient.astype(np.uint8)
        self._win.set_gradient(new_gradient)

    def _sort_cursors(self): # Sorts cursors based on their position along the slider
        self._cursors = sorted(self._cursors, key=lambda cursor: cursor.cursor_position)

    def _create_slider_buttons(self):
        self._add_cursor_button = Button(self._win.get_root(), text="Add +", command=self._add_cursor)
        self._add_cursor_button.place(x=self._x, y=1100, width=80, height=40)
        self._status_button = Button(self._win.get_root(), text="Status", command=self.cursor_status)
        self._status_button.place(x=self._x+90, y=1100, width=80, height=40)

    def _add_cursor(self):
        _cursor_to_add = GradientCursor(
            self,
            self._canvas,
            self._x,
            self._y,
            self._height,
            self._line_width,
            self._cursor_width,
            len(self._cursors),
            self._cursor_shades[len(self._cursors)]
        )
        self._cursors.append(_cursor_to_add)
        self.cursor_status()

    def cursor_status(self):
        print(self._cursors)

    def response_test(self):
        print("Hello!")

class Cursor: # TODO: Implement parent cursor class, make GradientCursor its child
    def __init__(self, canvas, x1, y1, width, height, slider_length):
        self._canvas = canvas

class GradientCursor:
    def __init__(self, slider, canvas, x1, y1, height, line_width, cursor_width, id = 0, shade = 0):
        self._slider = slider
        self._canvas = canvas
        self._id = id
        self._tag = "Cursor" + str(self._id)
        self.shade = shade

        self._height = height
        self._line_width = line_width

        self._cursor_width = cursor_width
        self._boundary_min = x1+line_width
        self._boundary_max = x1+slider.length-line_width

        self._create_cursor_elements()
        self._update_cursor_coords(x1+line_width,y1+line_width/2)

        self.cursor_position = 0
        self._clicked = False
    def __repr__(self):
        return f"{self._tag} at position {self.cursor_position} with shade {self.shade}"

    def _create_cursor_elements(self):
        self._line = self._canvas.create_line(0, 0, 0, 0, fill="red", width=self._line_width, dash=(8,2), tags=self._tag)
        self._triangle = self._canvas.create_polygon((0,0),(0,0),(0,0), fill="#666666", tags=self._tag)
        self._square = self._canvas.create_rectangle((0,0),(0,0), fill="black", tags=self._tag)
        self._canvas.tag_bind(self._tag, '<Button-1>', self.highlight_on)
        self._canvas.tag_bind(self._tag, '<B1-Motion>', self.move_x)
        self._canvas.tag_bind(self._tag, '<B1-ButtonRelease>', self.highlight_off)

    def _update_cursor_coords(self, x1, y1):
        self._canvas.coords(self._line,
                            (x1,y1),
                            (x1,y1+self._height-self._line_width))
        _line_bottom_x = self._canvas.coords(self._line)[2]
        _line_bottom_y = self._canvas.coords(self._line)[3]

        self._canvas.coords(self._triangle,
                            (_line_bottom_x, _line_bottom_y),
                            (_line_bottom_x+(self._cursor_width/2), _line_bottom_y+self._cursor_width),
                            (_line_bottom_x-(self._cursor_width/2), _line_bottom_y+self._cursor_width))
        
        _square_x1 = self._canvas.coords(self._triangle)[4]
        _square_y1 = self._canvas.coords(self._triangle)[3]
        _square_x2 = self._canvas.coords(self._triangle)[2]
        _square_y2 = self._canvas.coords(self._triangle)[3]+self._cursor_width
        self._canvas.coords(self._square,
                            (_square_x1,_square_y1),
                            (_square_x2,_square_y2))

    def _calculate_cursor_position(self, value):
        self.cursor_position = np.interp(value, [self._boundary_min, self._boundary_max], [0,1])
        self._slider.recalculate_gradient()

    def highlight_on(self, event):
        self._clicked = True
        self._canvas.itemconfig(self._triangle, fill="#AAAAAA")
        self._calculate_cursor_position(self._canvas.coords(self._line)[0])

    def highlight_off(self, event):
        self._clicked = False
        self._canvas.itemconfig(self._triangle, fill="#666666")

    def move_x(self, event):
        _x = min(max(self._boundary_min, event.x), self._boundary_max)
        self._update_cursor_coords(_x, self._canvas.coords(self._line)[1])
        self._calculate_cursor_position(_x)

    def set_x(self, x):
        _x = min(max(0, x), 1)
        _x = np.interp(_x, [0,1], [self._boundary_min, self._boundary_max])
        self._update_cursor_coords(_x, self._canvas.coords(self._line)[1])
        self._calculate_cursor_position(_x)