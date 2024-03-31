import tkinter as tk
from typing import List, Any, Tuple, Union, Optional
from tkinter import simpledialog
from settings import DEFAULT_TEXT_SIZE, DEFAULT_FONT, DEFAULT_TEXT_FONT, DEFAULT_TEXT_COLOR, BRUSH_DOT, BRUSH_POLYGON, \
    BRUSH_LINE


class Paint:
    def __init__(self, coords: Union[Tuple[Any, Any], Tuple[Any, Any, Any, Any]], width: int, color: str,
                 brush_style: str = BRUSH_DOT) -> None:
        """
        Initializes Paint parameters such as width and color, id on canvas and coordinates in format (x1, y1, x2, y2)
        :param coords: tuple of (x, y) or (x1, y1, x2, y2) coordinates
        :param width: width of the brush tool
        :param color: color of the brush tool
        :param brush_style: __figure to draw
        """
        self.__x1, self.__y1, self.__x2, self.__y2 = 0, 0, 0, 0
        self.__width = width
        self._set_coords(coords)
        self.__color = color
        self.id = None
        self.__figure = brush_style

    def _set_coords(self, coords: Union[Tuple[Any, Any], Tuple[Any, Any, Any, Any]]) -> None:
        if len(coords) == 2:
            self.__x1 = coords[0] - self.__width
            self.__y1 = coords[1] - self.__width
            self.__x2 = coords[0] + self.__width
            self.__y2 = coords[1] + self.__width
        else:
            self.__x1 = coords[0]
            self.__y1 = coords[1]
            self.__x2 = coords[2]
            self.__y2 = coords[3]

    def get_color(self) -> str:
        """
        Returns the color of the painted
        :return:
        """
        return self.__color

    def change_color(self, new_color: str, canvas: tk.Canvas) -> None:
        """
        Changing the color of the dot accordingly to the new color
        :param new_color: a new color of the paint
        :param canvas: the canvas that the paint belongs to
        :return: None
        """
        self.__color = new_color
        self._update_paint(canvas)

    def get_width(self) -> float:
        """
        Returns the width of the painted
        :return: the width of the painted
        """
        return self.__width

    def move(self, new_coords: Union[Tuple[Any, Any], Tuple[Any, Any, Any, Any]], canvas: tk.Canvas) -> None:
        """
        Moves the dot to the given position
        :param new_coords: new coordinates of the painted
        :param canvas: the canvas that the dot belongs to
        :return: None
        """
        self._set_coords(new_coords)
        self._update_paint(canvas)

    def _update_paint(self, canvas: tk.Canvas) -> None:
        """
        Function that updates the dot on the canvas
        :param canvas:  that the dot belongs to
        :return: None
        """
        try:
            canvas.delete(self.id)
            self.add_to_canvas(canvas)
        except IOError:
            print('Dot does not appear on canvas or canvas is not provided. There is nothing to change')

    def add_to_canvas(self, canvas: tk.Canvas) -> None:
        """
        Adds the dot to the canvas basing on coordinates
        :param canvas:
        :return:
        """
        if self.__figure == BRUSH_DOT:
            self.id = canvas.create_oval(self.__x1, self.__y1, self.__x2, self.__y2, fill=self.__color,
                                         outline=self.__color, width=self.__width)
        elif self.__figure == BRUSH_POLYGON:
            self.id = canvas.create_polygon(self.__x1, self.__y1, self.__x2, self.__y2, fill=self.__color,
                                            outline=self.__color, width=self.__width)
        elif self.__figure == BRUSH_LINE:
            self.id = canvas.create_line(self.__x1, self.__y1, self.__x2, self.__y2, fill=self.__color, width=self.__width)


class TextArea:
    def __init__(self, font_family: str, font_color: str, font_size: float, x: float = 20, y: float = 20,
                 text: str = 'Add text'):
        self.__x = x
        self.__y = y
        self.__font_family = font_family
        self.__font_size = font_size
        self.__text = text
        self.__text_color = font_color
        self.id = None

    def _update_text(self, canvas: tk.Canvas) -> None:
        try:
            if self.id is not None:
                canvas.delete(self.id)
            self.add_to_canvas(canvas)
        except IOError:
            print('Text does not appear on canvas or canvas is not provided. There is nothing to change')

    def add_to_canvas(self, canvas: tk.Canvas) -> None:
        self.id = canvas.create_text(self.__x, self.__y, text=self.__text, font=(self.__font_family, self.__font_size),
                                     fill=self.__text_color)

    def change_text(self, canvas: tk.Canvas) -> None:
        self.__text = simpledialog.askstring('Add text', "Enter text:", initialvalue=self.__text)
        self._update_text(canvas)

    def change_font(self, new_font_family: str, canvas: tk.Canvas) -> None:
        self.__font_family = new_font_family
        self._update_text(canvas)

    def change_font_size(self, new_font_size: float, canvas: tk.Canvas) -> None:
        self.__font_size = new_font_size
        self._update_text(canvas)


class Outline:
    def __init__(self, outline_color: str, width: float) -> None:
        self.__outline_color = outline_color
        self.__outline_width = width
        self.pixels = list()

    def change_outline_color(self, canvas, new_color) -> None:
        self.__outline_color = new_color
        for pixel in self.pixels:
            canvas.itemonfigure(pixel=pixel, color=self.__outline_color)
        canvas.update()

    def change_outline_width(self, canvas: tk.Canvas, new_width: float) -> None:
        self.__outline_width = new_width
        for pixel in self.pixels:
            canvas.itemconfigure(pixel=pixel, width=self.__outline_width)
        canvas.update()

    def get_outline_color(self):
        return self.__outline_color

    def get_outline_width(self):
        return self.__outline_width


class FillFigure:
    def __init__(self, fill_color: float = 'black'):
        self.__fill_color = fill_color

    def get_fill_color(self):
        return self.__fill_color

    def change_fill_color(self, new_color: str = 'black') -> None:
        self.__fill_color = new_color


class Painted:
    def __init__(self):
        self.__paints = list()

    def add_paint(self, paint: Paint) -> None:
        self.__paints.append(paint)

    def remove_paint(self, id_number: int) -> bool:
        for paint in self.__paints:
            if paint.id == id_number:
                self.__paints.remove(paint)
                return True
        return False

    def get_paint(self, id_number: int) -> Optional[Paint]:
        for paint in self.__paints:
            if paint.id == id_number:
                return paint

    def delete_from_canvas(self, canvas: tk.Canvas) -> None:
        for paint in self.__paints:
            canvas.delete(paint.id)

    def add_to_canvas(self, canvas: tk.Canvas) -> None:
        for paint in self.__paints:
            paint.add_to_canvas(canvas)


class Line(Outline):
    def __init__(self, color: str = 'black', width: float = 5.0) -> None:
        super().__init__(color, width)
        self.__id_numbers = list()

    def add_pixel(self, pixel: Tuple[Any, Any, Any, Any], canvas: tk.Canvas) -> None:
        self.pixels.append(pixel)
        result = canvas.create_line(*pixel, width=self.get_outline_width(), fill=self.get_outline_color())
        self.__id_numbers.append(result)

    def add_full_line(self, canvas: tk.Canvas) -> None:
        for pixel in self.pixels:
            canvas.create_line(*pixel, width=self.get_outline_width(), fill=self.get_outline_color())

    def delete_from_canvas(self, canvas) -> None:
        for number in self.__id_numbers:
            canvas.delete(number)
