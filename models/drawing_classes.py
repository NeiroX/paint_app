import tkinter as tk
from typing import List, Any, Tuple, Union, Optional
from tkinter import simpledialog
from settings import DEFAULT_TEXT_SIZE, DEFAULT_FONT, DEFAULT_TEXT_FONT, DEFAULT_TEXT_COLOR, RECTANGLE, TRIANGLE, OVAL


class Paint:
    def __init__(self, coords: Union[Tuple[Any, Any], Tuple[Any, Any, Any, Any]], width: int, color: str) -> None:
        """
        Initializes Paint parameters such as width and outline_color, id on canvas and coordinates in format (x1, y1, x2, y2)
        :param coords: tuple of (x, y) or (x1, y1, x2, y2) coordinates
        :param width: width of the brush tool
        :param color: outline_color of the brush tool
        """
        self.__x1, self.__y1, self.__x2, self.__y2 = 0, 0, 0, 0
        self.__width = width
        self._set_coords(coords)
        self.__color = color
        self.id = None

    def _set_coords(self, coords: Union[Tuple[Any, Any], Tuple[Any, Any, Any, Any]]) -> None:
        self.__x1 = coords[0] - self.__width
        self.__y1 = coords[1] - self.__width
        self.__x2 = coords[0] + self.__width
        self.__y2 = coords[1] + self.__width

    def get_color(self) -> str:
        """
        Returns the outline_color of the painted
        :return:
        """
        return self.__color

    def change_color(self, new_color: str, canvas: tk.Canvas) -> None:
        """
        Changing the outline_color of the dot accordingly to the new outline_color
        :param new_color: a new outline_color of the paint
        :param canvas: the canvas that the paint belongs to
        :return: None
        """
        self.__color = new_color
        self._update_paint(canvas)

    def change_width(self, new_width: int, canvas: tk.Canvas) -> None:
        self.__width = new_width
        self._update_paint(canvas)

    def get_width(self) -> float:
        """
        Returns the width of the painted
        :return: the width of the painted
        """
        return self.__width

    def move(self, x_delta: Union[float, int], y_delta: Union[float, int], canvas: tk.Canvas) -> None:
        """
        Moves the dot to the given position
        :param new_coords: new coordinates of the painted
        :param canvas: the canvas that the dot belongs to
        :return: None
        """
        self.__x1 += x_delta
        self.__y1 += y_delta
        self.__x2 += x_delta
        self.__y2 += y_delta
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
        except ValueError or IndexError:
            print('Dot does not appear on canvas or canvas is not provided. There is nothing to change')

    def add_to_canvas(self, canvas: tk.Canvas) -> None:
        """
        Adds the dot to the canvas basing on coordinates
        :param canvas:
        :return:
        """
        self.id = canvas.create_oval(self.__x1, self.__y1, self.__x2, self.__y2, fill=self.__color,
                                     outline=self.__color, width=self.__width)


class TextArea:
    def __init__(self, font_family: str, font_color: str, font_size: float, x: float = 20, y: float = 20,
                 text: str = 'Add text'):
        self.__x = x
        self.__y = y
        self.__font_family = font_family
        self.__font_size = font_size
        self.__text = text
        self.__font_color = font_color
        self.id = None

    def _update_text(self, canvas: tk.Canvas) -> None:
        try:
            if self.id is not None:
                canvas.delete(self.id)
            self.add_to_canvas(canvas)
        except ValueError or IndexError:
            print('Text does not appear on canvas or canvas is not provided. There is nothing to change')

    def add_to_canvas(self, canvas: tk.Canvas) -> None:
        self.id = canvas.create_text(self.__x, self.__y, text=self.__text, font=(self.__font_family, self.__font_size),
                                     fill=self.__font_color)

    def move(self, delta_x: float, delta_y: float, canvas: tk.Canvas) -> None:
        self.__x += delta_x
        self.__y += delta_y
        self._update_text(canvas)

    def change_text(self, canvas: tk.Canvas) -> None:
        self.__text = simpledialog.askstring('Add text', "Enter text:", initialvalue=self.__text)
        self._update_text(canvas)

    def change_font(self, new_font_family: str, canvas: tk.Canvas) -> None:
        self.__font_family = new_font_family
        self._update_text(canvas)

    def change_font_color(self, new_font_color: str, canvas: tk.Canvas) -> None:
        self.__font_color = new_font_color
        self._update_text(canvas)

    def change_font_size(self, new_font_size: float, canvas: tk.Canvas) -> None:
        self.__font_size = new_font_size
        self._update_text(canvas)


class Outline:
    def __init__(self, outline_color: str, width: float) -> None:
        self.__outline_color = outline_color
        self.__outline_width = width

    def change_outline_color(self, new_color) -> None:
        self.__outline_color = new_color

    def change_outline_width(self, new_width: float) -> None:
        self.__outline_width = new_width

    def get_outline_color(self):
        return self.__outline_color

    def get_outline_width(self):
        return self.__outline_width


class FillFigure:
    def __init__(self, fill_color: str = 'black'):
        self.__fill_color = fill_color

    def get_fill_color(self):
        return self.__fill_color

    def change_fill_color(self, new_color: str = 'black') -> None:
        self.__fill_color = new_color


class PaintGroup:
    def __init__(self, id_number: int):
        self.__paints = list()
        self.id = id_number

    def __contains__(self, id_number: int) -> bool:
        return id_number in list(map(lambda x: x.id, self.__paints))

    def add_paint(self, paint: Paint) -> None:
        self.__paints.append(paint)

    def move(self, x_delta: Union[float, int], y_delta: Union[float, int], canvas: tk.Canvas) -> None:
        for paint in self.__paints:
            paint.move(x_delta, y_delta, canvas=canvas)

    def remove_paint(self, id_number: int) -> bool:
        for paint in self.__paints:
            if paint.id == id_number:
                self.__paints.remove(paint)
                return True
        return False

    def change_color(self, new_color: str, canvas: tk.Canvas) -> None:
        for paint in self.__paints:
            paint.change_color(new_color, canvas)

    def change_width(self, new_width: int, canvas: tk.Canvas) -> None:
        for paint in self.__paints:
            paint.change_width(new_width, canvas)

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
    def __init__(self, outline_color: str = 'black', outline_width: float = 5.0, start_x: Any = 20,
                 start_y: Any = 20) -> None:
        super().__init__(outline_color, outline_width)
        self.id = None
        self.__start_x, self.__start_y = start_x, start_y
        self.__end_x, self.__end_y = start_x, start_y

    def add_to_canvas(self, canvas: tk.Canvas) -> None:
        self.id = canvas.create_line(self.__start_x, self.__start_y, self.__end_x, self.__end_y,
                                     width=self.get_outline_width(),
                                     fill=self.get_outline_color())

    def move(self, delta_x: float, delta_y: float, canvas: tk.Canvas) -> None:
        self.__start_x += delta_x
        self.__start_y += delta_y
        self.__end_x += delta_x
        self.__end_y += delta_y
        self.redraw(canvas)

    def delete_from_canvas(self, canvas: tk.Canvas) -> None:
        try:
            canvas.delete(self.id)

        except ValueError or IndexError:
            print("Object doesn't appear on canvas or canvas is not provided")

    def redraw(self, new_end_x: Any = None, new_end_y: Any = None, canvas: tk.Canvas = None) -> None:
        if new_end_x is not None and new_end_y is not None:
            self.__end_x, self.__end_y = new_end_x, new_end_y
        self.delete_from_canvas(canvas)
        self.add_to_canvas(canvas)


class Figure(Outline, FillFigure):
    def __init__(self, fill_color: str = 'black', outline_color: str = 'black', outline_width: int = 5,
                 start_x: Any = 20, start_y: Any = 20, figure_name: str = RECTANGLE) -> None:
        Outline.__init__(self, outline_color, outline_width)
        FillFigure.__init__(self, fill_color)
        self.id = None
        self.__start_x, self.__start_y = start_x, start_y
        self.__end_x, self.__end_y = start_x + 1, start_y + 1
        self.__name = figure_name

    def add_to_canvas(self, canvas: tk.Canvas) -> None:
        if self.__name == RECTANGLE:
            self.id = canvas.create_rectangle(self.__start_x, self.__start_y, self.__end_x, self.__end_y,
                                              width=self.get_outline_width(),
                                              fill=self.get_fill_color(), outline=self.get_outline_color())
        elif self.__name == TRIANGLE:
            vertices = [self.__start_x, self.__start_y, self.__end_x, self.__end_y, 2 * self.__start_x - self.__end_x,
                        self.__end_y]
            self.id = canvas.create_polygon(vertices, fill=self.get_fill_color(), outline=self.get_outline_color(),
                                            width=self.get_outline_width())
        elif self.__name == OVAL:
            self.id = canvas.create_oval(self.__start_x, self.__start_y, self.__end_x, self.__end_y,
                                         fill=self.get_fill_color(), outline=self.get_outline_color(),
                                         width=self.get_outline_width())

    def move(self, delta_x: float, delta_y: float, canvas: tk.Canvas) -> None:
        self.__start_x += delta_x
        self.__start_y += delta_y
        self.__end_x += delta_x
        self.__end_y += delta_y
        self.redraw(canvas)

    def delete_from_canvas(self, canvas: tk.Canvas) -> None:
        try:
            canvas.delete(self.id)
        except ValueError or IndexError:
            print("Object doesn't appear on canvas or canvas is not provided")

    def redraw(self, new_end_x: Any = None, new_end_y: Any = None, canvas: tk.Canvas = None) -> None:
        if new_end_x is not None and new_end_y is not None:
            self.__end_x, self.__end_y = new_end_x, new_end_y
        self.delete_from_canvas(canvas)
        self.add_to_canvas(canvas)
