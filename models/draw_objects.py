import tkinter as tk
from typing import List, Any, Tuple, Union, Optional
from tkinter import simpledialog
from settings import DEFAULT_TEXT_SIZE, DEFAULT_FONT, DEFAULT_TEXT_FONT, DEFAULT_TEXT_COLOR, RECTANGLE, TRIANGLE, OVAL, \
    POLYGON, DEFAULT_BRUSH_COLOR, DEFAULT_BRUSH_SIZE


class Paint:
    def __init__(self, coords: Tuple[Any, Any], width: int, color: str, id_number: int = None) -> None:
        """
        Initializes Paint parameters such as width and outline_color, id on canvas and coordinates in format (x1, y1, x2, y2)
        :param coords: tuple of (x, y) coordinates
        :param width: width of the brush tool
        :param color: outline_color of the brush tool
        """
        self.__x1, self.__y1, self.__x2, self.__y2 = 0, 0, 0, 0
        self.__width = width
        self._set_coords(coords)
        self.__color = color
        self.id = None

    def copy(self) -> 'Paint':
        return Paint((self.__x1 + self.__width, self.__y1 + self.__width), self.__width, self.__color, self.id)

    def _set_coords(self, coords: Tuple[Any, Any]) -> None:
        """
        Centring dot to the given position according to brush width
        :param coords: tuple of (x, y) coordinates
        :return: None
        """
        self.__x1 = coords[0] - self.__width
        self.__y1 = coords[1] - self.__width
        self.__x2 = coords[0] + self.__width
        self.__y2 = coords[1] + self.__width

    def get_color(self) -> str:
        """
        Returns the outline_color of the painted dot
        :return color: a color of the painted dot
        """
        return self.__color

    def change_color(self, new_color: str, canvas: tk.Canvas) -> None:
        """
        Changing the outline color of the dot accordingly to the new outline color
        :param new_color: a new outline color of the painted dot
        :param canvas: the canvas that the painted dot belongs to
        :return: None
        """
        self.__color = new_color
        self._update_paint(canvas)

    def change_width(self, new_width: int, canvas: tk.Canvas) -> None:
        """
        Changing the outline width of the dot
        :param new_width: a new outline width of the painted dot
        :param canvas: the canvas that the painted dot belongs to
        :return: None
        """
        self.__width = new_width
        self._update_paint(canvas)

    def get_width(self) -> float:
        """
        Returns the width of the painted dot
        :return width: the width of the painted dot
        """
        return self.__width

    def move(self, x_delta: float, y_delta: float, canvas: tk.Canvas) -> None:
        """
        Moves the dot to the given position
        :param x_delta: delta of movement on X axis
        :param y_delta: delta of movement on Y axis
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
    def __init__(self, font_family: str, font_color: str, font_size: int, x: float = 20, y: float = 20,
                 text: str = 'Add text') -> None:
        self.__x = x
        self.__y = y
        self.__font_family = font_family
        self.__font_size = font_size
        self.__text = text
        self.__font_color = font_color
        self.id = None

    def copy(self) -> 'TextArea':

        return TextArea(self.__font_family, self.__font_color, self.__font_size, self.__x, self.__y, self.__text)

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

    def change_font_family(self, new_font_family: str, canvas: tk.Canvas) -> None:
        self.__font_family = new_font_family
        self._update_text(canvas)

    def change_font_color(self, new_font_color: str, canvas: tk.Canvas) -> None:
        self.__font_color = new_font_color
        self._update_text(canvas)

    def change_font_size(self, new_font_size: int, canvas: tk.Canvas) -> None:
        self.__font_size = new_font_size
        self._update_text(canvas)

    def get_font_size(self) -> int:
        return self.__font_size

    def get_font_family(self) -> str:
        return self.__font_family

    def get_font_color(self) -> str:
        return self.__font_color


class Outline:
    def __init__(self, outline_color: str, width: int) -> None:
        self.__outline_color = outline_color
        self.__outline_width = width

    def change_outline_color(self, new_color) -> None:
        self.__outline_color = new_color

    def change_outline_width(self, new_width: float) -> None:
        self.__outline_width = new_width

    def get_outline_color(self) -> str:
        return self.__outline_color

    def get_outline_width(self) -> int:
        return self.__outline_width


class FillFigure:
    def __init__(self, fill_color: str = 'black') -> None:
        self.__fill_color = fill_color

    def get_fill_color(self) -> str:
        return self.__fill_color

    def change_fill_color(self, new_color: str = 'black') -> None:
        self.__fill_color = new_color


class PaintGroup:
    def __init__(self, id_number: int, paints: List[Paint] = None) -> None:
        self.__paints = list() if paints is None else paints
        self.id = id_number

    def __contains__(self, id_number: int) -> bool:
        return id_number in list(map(lambda x: x.id, self.__paints))

    def copy(self) -> 'PaintGroup':
        new_paints = list()
        for p in self.__paints:
            new_paints.append(p.copy())
        return PaintGroup(self.id, new_paints)

    def add_paint(self, paint: Paint) -> None:
        self.__paints.append(paint)

    def move(self, x_delta: Union[float, int], y_delta: Union[float, int], canvas: tk.Canvas) -> None:
        for paint in self.__paints:
            paint.move(x_delta, y_delta, canvas=canvas)

    def bring_forward(self, canvas: tk.Canvas) -> None:
        for paint in self.__paints:
            canvas.tag_raise(paint.id)

    def send_backward(self, canvas: tk.Canvas) -> None:
        for paint in self.__paints:
            canvas.tag_lower(paint.id)

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

    def get_color(self) -> str:
        if self.__paints:
            return self.__paints[0].get_color()
        return DEFAULT_BRUSH_COLOR

    def get_width(self) -> int:
        if self.__paints:
            return self.__paints[0].get_width()
        return DEFAULT_BRUSH_SIZE


class Line(Outline):
    def __init__(self, outline_color: str = 'black', outline_width: float = 5.0, start_x: Any = 20,
                 start_y: Any = 20, end_x: Any = None, end_y: Any = None) -> None:
        super().__init__(outline_color, outline_width)
        self.id = None
        self.__start_x, self.__start_y = start_x, start_y
        if end_x is not None and end_y is not None:
            self.__end_x, self.__end_y = end_x, end_y
        else:
            self.__end_x, self.__end_y = start_x, start_y

    def copy(self) -> 'Line':
        return Line(self.get_outline_color(), self.get_outline_width(), self.__start_x, self.__start_y, self.__end_x,
                    self.__end_y)

    def add_to_canvas(self, canvas: tk.Canvas) -> None:
        self.id = canvas.create_line(self.__start_x, self.__start_y, self.__end_x, self.__end_y,
                                     width=self.get_outline_width(),
                                     fill=self.get_outline_color())

    def move(self, delta_x: float, delta_y: float, canvas: tk.Canvas) -> None:
        self.__start_x += delta_x
        self.__start_y += delta_y
        self.__end_x += delta_x
        self.__end_y += delta_y
        self.redraw(canvas=canvas)

    def delete_from_canvas(self, canvas: tk.Canvas) -> None:
        try:
            canvas.delete(self.id)

        except AttributeError or IndexError:
            print("Object doesn't appear on canvas or canvas is not provided")

    def redraw(self, new_end_x: Any = None, new_end_y: Any = None, canvas: tk.Canvas = None) -> None:
        if new_end_x is not None and new_end_y is not None:
            self.__end_x, self.__end_y = new_end_x, new_end_y
        self.delete_from_canvas(canvas=canvas)
        self.add_to_canvas(canvas=canvas)


class Figure(Outline, FillFigure):
    def __init__(self, fill_color: str = 'black', outline_color: str = 'black', outline_width: int = 5,
                 start_x: Any = 20, start_y: Any = 20, figure_name: str = RECTANGLE, end_x: Any = None,
                 end_y: Any = None, vertices_of_polygon: List[Any] = None) -> None:
        Outline.__init__(self, outline_color, outline_width)
        FillFigure.__init__(self, fill_color)
        self.id = None
        self.__start_x, self.__start_y = start_x, start_y
        if end_x is None and end_y is None:
            self.__end_x, self.__end_y = start_x + 1, start_y + 1
        else:
            self.__end_x, self.__end_y = end_x, end_y
        self.__name = figure_name
        if vertices_of_polygon is not None:
            self.__vertices_of_polygon = vertices_of_polygon
        else:
            self.__vertices_of_polygon = [start_x, start_y]

    def copy(self) -> 'Figure':
        return Figure(self.get_fill_color(), self.get_outline_color(), self.get_outline_width(), self.__start_x,
                      self.__start_y, self.__name, self.__end_x, self.__end_y, self.__vertices_of_polygon.copy())

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
        elif self.__name == POLYGON:
            self.id = canvas.create_polygon(self.__vertices_of_polygon,
                                            fill=self.get_fill_color(),
                                            outline=self.get_outline_color(),
                                            width=self.get_outline_width())

    def move(self, delta_x: float, delta_y: float, canvas: tk.Canvas) -> None:
        if self.__name != POLYGON:
            self.__start_x += delta_x
            self.__start_y += delta_y
            self.__end_x += delta_x
            self.__end_y += delta_y
        elif self.__name == POLYGON:
            for i in range(0, len(self.__vertices_of_polygon), 2):
                self.__vertices_of_polygon[i] += delta_x
                self.__vertices_of_polygon[i + 1] += delta_y
        self.redraw(canvas=canvas)

    def get_figure_name(self) -> str:
        return self.__name

    def add_vertex(self, vertex_x: float, vertex_y: float, canvas: tk.Canvas, replace_old: bool = False) -> None:
        if replace_old:
            self.__vertices_of_polygon[-1] = vertex_y
            self.__vertices_of_polygon[-2] = vertex_x
        else:
            self.__vertices_of_polygon.append(vertex_x)
            self.__vertices_of_polygon.append(vertex_y)
        self.redraw(canvas=canvas)

    def delete_last_vertex(self, canvas: tk.Canvas) -> None:
        if len(self.__vertices_of_polygon) > 2:
            del self.__vertices_of_polygon[-1]
            del self.__vertices_of_polygon[-1]
            self.redraw(canvas=canvas)

    def delete_from_canvas(self, canvas: tk.Canvas) -> None:
        try:
            canvas.delete(self.id)
        except AttributeError:
            print("Object doesn't appear on canvas or canvas is not provided")

    def redraw(self, new_end_x: Any = None, new_end_y: Any = None, canvas: tk.Canvas = None) -> None:
        if new_end_x is not None and new_end_y is not None:
            self.__end_x, self.__end_y = new_end_x, new_end_y
        self.delete_from_canvas(canvas=canvas)
        self.add_to_canvas(canvas=canvas)
