import tkinter as tk
from settings import BRUSH_DOT, DEFAULT_TEXT_FONT, DEFAULT_TEXT_SIZE, DEFAULT_TEXT_COLOR
from typing import Any, Tuple
from tkinter import simpledialog


class BasicTool:
    def __init__(self, width: int = 5, color: str = 'black'):
        self.__width = width
        self.__color = color

    def change_tool_color(self, new_color: str = 'black'):
        self.__color = new_color

    def change_tool_width(self, new_width: int = 5):
        self.__width = new_width

    def get_width(self) -> int:
        return self.__width

    def get_color(self) -> str:
        return self.__color


class Brush(BasicTool):
    def __init__(self, width: int, color: str = 'black'):
        super().__init__(width, color)
        self.__brush_style = BRUSH_DOT

    def change_brush_style(self, new_style: str):
        self.__brush_style = new_style

    def get_brush_style(self) -> str:
        return self.__brush_style


class Eraser(BasicTool):
    def __init__(self, width: int, color: str = 'white', remove_object: bool = True) -> None:
        super().__init__(width, color)
        self._remove_object = True

    def change_eraser_work(self, remove_object: bool) -> None:
        self._remove_object = remove_object

    def get_eraser_work(self) -> bool:
        return self._remove_object

class Texting:
    def __init__(self, font_family: str = DEFAULT_TEXT_FONT, font_size: int = DEFAULT_TEXT_SIZE,
                 font_color: str = DEFAULT_TEXT_COLOR):
        self.__font_family = font_family
        self.__font_size = font_size
        self.__font_color = font_color

    def get_font_family(self) -> str:
        return self.__font_family

    def get_font_size(self) -> int:
        return self.__font_size

    def get_font_color(self) -> str:
        return self.__font_color

    def change_font_family(self, new_font_family: str) -> None:
        self.__font_family = new_font_family

    def change_font_size(self, new_font_size: int) -> None:
        self.__font_size = new_font_size

    def change_font_color(self, new_font_color: str) -> None:
        self.__font_color = new_font_color
