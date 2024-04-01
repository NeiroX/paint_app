from settings import (DEFAULT_BRUSH_SIZE, DEFAULT_BRUSH_COLOR, DEFAULT_TEXT_FONT,
                      DEFAULT_TEXT_SIZE, DEFAULT_TEXT_COLOR, LINE)


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
    def __init__(self, width: int = DEFAULT_BRUSH_SIZE, color: str = DEFAULT_BRUSH_COLOR):
        super().__init__(width, color)


class Eraser(BasicTool):
    def __init__(self, width: int, color: str = 'white') -> None:
        super().__init__(width, color)


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


class FigureDrawing:
    def __init__(self, fill_color: str = 'black', outline_color: str = 'black', outline_width: int = 5,
                 current_figure: str = LINE):
        self.__fill_color = fill_color
        self.__outline_color = outline_color
        self.__outline_width = outline_width
        self.__current_figure = current_figure

    def change_fill_color(self, new_color: str) -> None:
        self.__fill_color = new_color

    def change_outline_color(self, new_color: str) -> None:
        self.__outline_color = new_color

    def change_outline_width(self, new_width: int) -> None:
        self.__outline_width = new_width

    def change_figure(self, new_figure: str) -> None:
        self.__current_figure = new_figure

    def get_current_figure(self) -> str:
        return self.__current_figure

    def get_outline_color(self) -> str:
        return self.__outline_color

    def get_outline_width(self) -> int:
        return self.__outline_width

    def get_fill_color(self) -> str:
        return self.__fill_color
