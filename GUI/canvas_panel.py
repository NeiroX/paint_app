import tkinter as tk
from models.changes import BackgroundChange
from settings import *


class CanvasPanel(tk.Canvas):
    def __init__(self, master: tk.Tk, width: int, height: int, background_color: str = DEFAULT_CANVAS_COLOR) -> None:
        super().__init__(master, width=width, height=height, background=background_color, cursor='circle')
        self.__background_color = background_color

    def change_background_color(self, new_color: str) -> BackgroundChange:
        new_background_change = BackgroundChange(self.__background_color, new_color)
        self.configure(background=new_color)
        self.__background_color = new_color
        return new_background_change

    def reset_background_color(self) -> None:
        self.configure(background=DEFAULT_CANVAS_COLOR)

    def custom_pack(self) -> None:
        self.pack(fill=tk.BOTH, expand=True)
