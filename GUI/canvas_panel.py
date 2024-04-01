import tkinter as tk
from models.changes import BackgroundChange
from settings import *
from PIL import Image
import time


class CanvasPanel(tk.Canvas):
    """
    Custom canvas that inherits from tkinter.Canvas
    """

    def __init__(self, master: tk.Tk, width: int, height: int, background_color: str = DEFAULT_CANVAS_COLOR) -> None:
        """
        Constructor for
        :param master: window object for canvas to be placed on
        :param width: width of the canvas from type int
        :param height: height of the canvas from type int
        :param background_color: color of canvas background from type string
        :return: None
        """
        super().__init__(master, width=width, height=height, background=background_color, cursor='circle')
        self.__background_color = background_color

    def change_background_color(self, new_color: str) -> BackgroundChange:
        """
        Function that changes the background color of the canvas and save change in type BackgroundChange
        :param new_color: a new color for the canvas background
        :return: BackgroundChange object that contains changes
        """
        new_background_change = BackgroundChange(self.__background_color, new_color)
        self.configure(background=new_color)
        self.__background_color = new_color
        return new_background_change

    def reset_background_color(self) -> None:
        """
        Function that resets the background of the canvas
        :return: None
        """
        self.configure(background=DEFAULT_CANVAS_COLOR)

    def custom_pack(self) -> None:
        """
        Custom pack of canvas on window
        :return: None
        """
        self.pack(fill=tk.BOTH, expand=True)

    def save(self) -> None:
        """
        Function that saves the canvas to image
        :return: None
        """
        try:
            image_file_name = 'result'
            path_to_save = os.path.join(BASE_DIR, image_file_name)
            self.postscript(file=path_to_save + '.ps', colormode='color')
            time.sleep(5)
            psimage = Image.open(path_to_save + '.ps')
            psimage.save(path_to_save + '.jpg')
            print('Image saved to ' + path_to_save)
        except OSError as e:
            print("Can't save image. Next error is raised:\n", e)

