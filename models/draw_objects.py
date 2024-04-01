import tkinter as tk
from typing import List, Any, Tuple, Union, Optional, Dict
from tkinter import simpledialog
from settings import DEFAULT_TEXT_SIZE, DEFAULT_FONT, DEFAULT_TEXT_FONT, DEFAULT_TEXT_COLOR, RECTANGLE, TRIANGLE, OVAL, \
    POLYGON, DEFAULT_BRUSH_COLOR, DEFAULT_BRUSH_SIZE


class Paint:
    def __init__(self, coords: Tuple[Any, Any], width: int, color: str, id_number: int = None) -> None:
        """
        Initializes Paint parameters such as width and outline_color, id on canvas and coordinates in format (x1, y1, x2, y2)
        :param coords: tuple of (x, y) coordinates
        :param width: width of the brush tool
        :param color: color of the brush tool
        """
        self.__x1, self.__y1, self.__x2, self.__y2 = 0, 0, 0, 0
        self.__width = width
        self._set_coords(coords)
        self.__color = color
        self.id = None

    def copy(self) -> 'Paint':
        return Paint((self.__x1 + self.__width, self.__y1 + self.__width), self.__width, self.__color, self.id)

    def save_settings_to_dict(self) -> Dict[str, Any]:
        """
        Save all the parameters of the painted dot object into a dictionary
        :return: the dictionary with parameters
        """
        parameters = dict()
        parameters['coords'] = (self.__x1 + self.__width, self.__y1 + self.__width)
        parameters['width'] = self.__width
        parameters['color'] = self.__color
        parameters['id'] = self.id
        return parameters

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

    @staticmethod
    def load_from_dict(settings: Dict[str, Any]) -> 'Paint':
        """
        Loads the painted dot from a dictionary settings and returns Paint object
        :param settings: dictionary with painted dot settings
        :return: object from Paint class
        """
        coords = settings['coords']
        width = settings['width']
        color = settings['color']
        return Paint(coords, width, color)


class PaintGroup:
    """
    Class that represents one brush use, in other words a group of painted dots until first LMB release
    """

    def __init__(self, id_number: int, paints: List[Paint] = None) -> None:
        """
        Initializes the group of painted dots
        :param id_number: id of painted dots group
        :param paints: optional parameter representing the painted dots list
        """
        self.__paints = list() if paints is None else paints
        self.id = id_number

    def __contains__(self, id_number: int) -> bool:
        """
        Checks if the painted dot with the given id is within this group
        :param id_number: id number of painted dot
        :return: result whether painted dot is within this group
        """
        return id_number in list(map(lambda x: x.id, self.__paints))

    def copy(self) -> 'PaintGroup':
        """
        Creates a copy of the current group
        :return: new group of painted dots
        """
        new_paints = list()
        for p in self.__paints:
            new_paints.append(p.copy())
        return PaintGroup(self.id, new_paints)

    def save_settings_to_dict(self) -> Dict[str, Any]:
        """
        Save all the parameters of the painted group object into a dictionary
        :return: the dictionary with parameters
        """
        parameters = dict()
        parameters['paints'] = list()
        for p in self.__paints:
            parameters['paints'].append(p.save_settings_to_dict())
        parameters['id'] = self.id
        return parameters

    def add_paint(self, paint: Paint) -> None:
        """
        Adds a painted dot to the group
        :param paint: painted dot from type Paint
        :return: None
        """
        self.__paints.append(paint)

    def move(self, x_delta: Union[float, int], y_delta: Union[float, int], canvas: tk.Canvas) -> None:
        """
        Moves all painted dots in group
        :param x_delta: change X axis direction
        :param y_delta: change Y axis direction
        :param canvas: a canvas which contains the painted dots of group
        :return: None
        """
        for paint in self.__paints:
            paint.move(x_delta, y_delta, canvas=canvas)

    def bring_forward(self, canvas: tk.Canvas) -> None:
        """
        Brings all painted dots of group forward on canvas
        :param canvas: a canvas which contains the painted dots of group
        :return: None
        """
        for paint in self.__paints:
            if paint.id is None:
                paint.add_to_canvas(canvas)
            canvas.tag_raise(paint.id)

    def send_backward(self, canvas: tk.Canvas) -> None:
        """
        Sends all painted dots of group backward on canvas
        :param canvas: a canvas which contains the painted dots of group
        :return: None
        """
        for paint in self.__paints:
            if paint.id is None:
                paint.add_to_canvas(canvas)
            canvas.tag_lower(paint.id)

    def remove_paint(self, id_number: int) -> bool:
        """
        Removes a painted dot from group
        :param id_number: id number of dot to remove
        :return: result whether dot was removed or not
        """
        for paint in self.__paints:
            if paint.id == id_number:
                self.__paints.remove(paint)
                return True
        return False

    def change_color(self, new_color: str, canvas: tk.Canvas) -> None:
        """
        Changes the color of the all painted dots in group
        :param new_color: new color of dot
        :param canvas: a canvas which contains the painted dots of group
        :return: None
        """
        for paint in self.__paints:
            paint.change_color(new_color, canvas)

    def change_width(self, new_width: int, canvas: tk.Canvas) -> None:
        """
        Changes the width of the all painted dots in group
        :param new_width: new width of dot
        :param canvas: a canvas which contains the painted dots of group
        :return: None
        """
        for paint in self.__paints:
            paint.change_width(new_width, canvas)

    def get_paint(self, id_number: int) -> Optional[Paint]:
        """
        Returns the painted dot object if it exists, otherwise None
        :param id_number: id number of dot
        :return: a painted dot object if it exists, otherwise None
        """
        for paint in self.__paints:
            if paint.id == id_number:
                return paint

    def delete_from_canvas(self, canvas: tk.Canvas) -> None:
        """
        Deletes the group of painted dots from the canvas
        :param canvas: a canvas which contains the painted dots of group
        :return: None
        """
        for paint in self.__paints:
            canvas.delete(paint.id)

    def add_to_canvas(self, canvas: tk.Canvas) -> None:
        """
        Adds the group of painted dots to the canvas
        :param canvas: a canvas which contains the painted dots of group
        :return: None
        """
        for paint in self.__paints:
            paint.add_to_canvas(canvas)

    def get_color(self) -> str:
        """
        Returns the color of the painted dots
        :return: color of the painted dots from type string
        """
        if self.__paints:
            return self.__paints[0].get_color()
        return DEFAULT_BRUSH_COLOR

    def get_width(self) -> int:
        """
        Returns the width of the painted dots
        :return: returns the width of the painted dots from type int
        """
        if self.__paints:
            return self.__paints[0].get_width()
        return DEFAULT_BRUSH_SIZE

    @staticmethod
    def load_from_dict(settings: Dict[str, Any]) -> 'PaintGroup':
        """
        Loads the group of painted dots from a dictionary settings and returns PaintGroup object
        :param settings: dictionary with group of painted dots settings
        :return: object from PaintGroup class
        """
        paints = list()
        id_number = settings["id"]
        for paint in settings['paints']:
            paints.append(Paint.load_from_dict(paint))
        return PaintGroup(id_number, paints)


class TextArea:
    """
    Class representing a text area on the canvas
    """

    def __init__(self, font_family: str, font_color: str, font_size: int, x: float = 20, y: float = 20,
                 text: str = 'Add text') -> None:
        """
        Initializes the text area with the given parameters
        :param font_family: font family of text on canvas
        :param font_color: text color on canvas
        :param font_size: font size
        :param x: x position of the object
        :param y: y position of the object
        :param text: a text to display on the canvas
        """
        self.__x = x
        self.__y = y
        self.__font_family = font_family
        self.__font_size = font_size
        self.__text = text
        self.__font_color = font_color
        self.id = None

    def copy(self) -> 'TextArea':
        """
        Returns a copy of the current text object
        :return: a copy of the object
        """

        return TextArea(self.__font_family, self.__font_color, self.__font_size, self.__x, self.__y, self.__text)

    def save_settings_to_dict(self) -> Dict[str, Any]:
        """
        Save all the parameters of the text object into a dictionary
        :return: the dictionary with parameters
        """
        parameters = dict()
        parameters['font_family'] = self.__font_family
        parameters['font_color'] = self.__font_color
        parameters['font_size'] = self.__font_size
        parameters['text'] = self.__text
        parameters['x'] = self.__x
        parameters['y'] = self.__y
        return parameters

    def _update_text(self, canvas: tk.Canvas) -> None:
        """
        Updates the text on the canvas
        :param canvas: a canvas which contains the text object
        :return: None
        """
        try:
            if self.id is not None:
                canvas.delete(self.id)
            self.add_to_canvas(canvas)
        except ValueError or IndexError:
            print('Text does not appear on canvas or canvas is not provided. There is nothing to change')

    def add_to_canvas(self, canvas: tk.Canvas) -> None:
        """
        Adds the text object to the canvas
        :param canvas: a canvas which contains the text object
        :return: None
        """
        self.id = canvas.create_text(self.__x, self.__y, text=self.__text, font=(self.__font_family, self.__font_size),
                                     fill=self.__font_color)

    def move(self, delta_x: float, delta_y: float, canvas: tk.Canvas) -> None:
        """
        Moves the text object on canvas
        :param delta_x: change X axis
        :param delta_y: change Y axis
        :param canvas: a canvas which contains the text object
        :return: None
        """
        self.__x += delta_x
        self.__y += delta_y
        self._update_text(canvas)

    def change_text(self, canvas: tk.Canvas) -> None:
        """
        Calls dialog window to change the text of text object
        :param canvas: a canvas which contains the text object
        :return: None
        """
        self.__text = simpledialog.askstring('Add text', "Enter text:", initialvalue=self.__text)
        self._update_text(canvas)

    def change_font_family(self, new_font_family: str, canvas: tk.Canvas) -> None:
        """
        Changes the font family of the text object on canvas
        :param new_font_family: name of the new font family from type string
        :param canvas: a canvas which contains the text object
        :return: None
        """
        self.__font_family = new_font_family
        self._update_text(canvas)

    def change_font_color(self, new_font_color: str, canvas: tk.Canvas) -> None:
        """
        Changes the font color of the text object on canvas
        :param new_font_color: a new font color from type string
        :param canvas: a canvas which contains the text object
        :return: None
        """
        self.__font_color = new_font_color
        self._update_text(canvas)

    def change_font_size(self, new_font_size: int, canvas: tk.Canvas) -> None:
        """
        Changes the font size of the text object on canvas
        :param new_font_size: a new font size from type int
        :param canvas: a canvas which contains the text object
        :return: None
        """
        self.__font_size = new_font_size
        self._update_text(canvas)

    def get_font_size(self) -> int:
        """
        Returns current font size of the text object
        :return: font size of the text object from type int
        """
        return self.__font_size

    def get_font_family(self) -> str:
        """
        Returns current font family of the text object
        :return: name of font family from type string
        """
        return self.__font_family

    def get_font_color(self) -> str:
        """
        Returns current font color of the text object
        :return: current font color from type string
        """
        return self.__font_color

    @staticmethod
    def load_from_dict(settings: Dict[str, Any]) -> 'TextArea':
        """
        Loads the text from a dictionary settings and returns TextArea object
        :param settings: dictionary with text settings
        :return: object from TextArea class
        """
        font_family = settings['font_family']
        font_color = settings['font_color']
        font_size = settings['font_size']
        text = settings['text']
        x = settings['x']
        y = settings['y']

        return TextArea(font_family, font_color, font_size, x, y, text)


class Outline:
    """
    Class representing the outline of figures
    """

    def __init__(self, outline_color: str, width: int) -> None:
        """
        Initializes the outline of figures with the given parameters
        :param outline_color: color of the outline
        :param width: thickness of the outline
        """
        self.__outline_color = outline_color
        self.__outline_width = width

    def change_outline_color(self, new_color) -> None:
        """
        Changes the outline color of figure
        :param new_color: new color of the outline
        :return: None
        """
        self.__outline_color = new_color

    def change_outline_width(self, new_width: float) -> None:
        """
        Changes the outline width of figure
        :param new_width: new width of the outline
        :return: None
        """
        self.__outline_width = new_width

    def get_outline_color(self) -> str:
        """
        Returns the color of the outline
        :return: an outline color from type string
        """
        return self.__outline_color

    def get_outline_width(self) -> int:
        """
        Returns the width of the outline
        :return: a width of the outline
        """
        return self.__outline_width


class FillFigure:
    """
    Class representing the fill of figures
    """

    def __init__(self, fill_color: str = 'black') -> None:
        """
        Initializes the fill of figures with the given parameters
        :param fill_color: color of fill
        :return: None
        """
        self.__fill_color = fill_color

    def get_fill_color(self) -> str:
        """
        Returns the color of the fill
        :return: color of the fill from type string
        """
        return self.__fill_color

    def change_fill_color(self, new_color: str = 'black') -> None:
        """
        Changes the color of the figure fill
        :param new_color: new color of the fill from type string
        :return: None
        """
        self.__fill_color = new_color


class Line(Outline):
    """
    Class representing the line figure on the canvas. It inherits from Outline and doesn't have filling
    """

    def __init__(self, outline_color: str = 'black', outline_width: float = 5.0, start_x: Any = 20,
                 start_y: Any = 20, end_x: Any = None, end_y: Any = None) -> None:
        """
        Initializes the line figure on the canvas
        :param outline_color: outline color of the line
        :param outline_width: outline thickness of the line
        :param start_x: starting x position of the line
        :param start_y: starting y position of the line
        :param end_x: ending x position of the line (optional parameter)
        :param end_y: ending y position of the line (optional parameter)
        """
        super().__init__(outline_color, outline_width)
        self.id = None
        self.__start_x, self.__start_y = start_x, start_y
        if end_x is not None and end_y is not None:
            self.__end_x, self.__end_y = end_x, end_y
        else:
            self.__end_x, self.__end_y = start_x, start_y

    def save_settings_to_dict(self) -> Dict[str, Any]:
        """
        Save all the parameters of the line object into a dictionary
        :return: the dictionary with parameters
        """
        parameters = dict()
        parameters['outline_color'] = self.get_outline_color()
        parameters['outline_width'] = self.get_outline_width()
        parameters['start_x'] = self.__start_x
        parameters['start_y'] = self.__start_y
        parameters['end_x'] = self.__end_x
        parameters['end_y'] = self.__end_y
        return parameters

    def copy(self) -> 'Line':
        """
        Creates a copy of the line figure object
        :return: copy object
        """
        return Line(self.get_outline_color(), self.get_outline_width(), self.__start_x, self.__start_y, self.__end_x,
                    self.__end_y)

    def add_to_canvas(self, canvas: tk.Canvas) -> None:
        """
        Adds the line to the canvas
        :param canvas: a canvas which contains the line object
        :return: None
        """
        self.id = canvas.create_line(self.__start_x, self.__start_y, self.__end_x, self.__end_y,
                                     width=self.get_outline_width(),
                                     fill=self.get_outline_color())

    def move(self, delta_x: float, delta_y: float, canvas: tk.Canvas) -> None:
        """
        Moves the line on canvas
        :param delta_x: change X axis
        :param delta_y: change Y axis
        :param canvas: a canvas which contains the line object
        :return: None
        """
        self.__start_x += delta_x
        self.__start_y += delta_y
        self.__end_x += delta_x
        self.__end_y += delta_y
        self.redraw(canvas=canvas)

    def delete_from_canvas(self, canvas: tk.Canvas) -> None:
        """
        Deletes the line from the canvas
        :param canvas: a canvas which contains the line object
        :return: None
        """
        try:
            canvas.delete(self.id)

        except AttributeError or IndexError:
            print("Object doesn't appear on canvas or canvas is not provided")

    def redraw(self, new_end_x: Any = None, new_end_y: Any = None, canvas: tk.Canvas = None) -> None:
        """
        Redraws the line on canvas with new coordinates if line is drawing
        :param new_end_x: optional new end line x position
        :param new_end_y: optional new end line y position
        :param canvas: a canvas which contains the line object
        :return: None
        """
        if new_end_x is not None and new_end_y is not None:
            self.__end_x, self.__end_y = new_end_x, new_end_y
        self.delete_from_canvas(canvas=canvas)
        self.add_to_canvas(canvas=canvas)

    @staticmethod
    def load_from_dict(settings: dict) -> 'Line':
        """
        Loads the line from a dictionary settings and returns Line object
        :param settings: dictionary with line settings
        :return: object from Line class
        """
        outline_color = settings['outline_color']
        outline_width = settings['outline_width']
        start_x = settings['start_x']
        start_y = settings['start_y']
        end_x = settings['end_x']
        end_y = settings['end_y']
        return Line(outline_color=outline_color, outline_width=outline_width, start_x=start_x, start_y=start_y,
                    end_x=end_x, end_y=end_y)


class Figure(Outline, FillFigure):
    """
    Class representing a figure on the canvas. It inherits from Outline and FillFigure
    """

    def __init__(self, fill_color: str = 'black', outline_color: str = 'black', outline_width: int = 5,
                 start_x: Any = 20, start_y: Any = 20, figure_name: str = RECTANGLE, end_x: Any = None,
                 end_y: Any = None, vertices_of_polygon: List[Any] = None) -> None:
        """
        Initializes the figure on the canvas with given parameters
        :param fill_color: color of figure filling
        :param outline_color: color of the figure outline
        :param outline_width: width of the figure outline
        :param start_x: start x position of the figure
        :param start_y: start y position of the figure
        :param figure_name: name of the figure to draw
        :param end_x: optional end x position
        :param end_y: optional end y position
        :param vertices_of_polygon: optional list of vertices of the polygon
        """
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
        """
        Returns a copy of the figure object
        :return: copy object
        """
        return Figure(self.get_fill_color(), self.get_outline_color(), self.get_outline_width(), self.__start_x,
                      self.__start_y, self.__name, self.__end_x, self.__end_y, self.__vertices_of_polygon.copy())

    def save_settings_to_dict(self) -> Dict[str, Any]:
        """
        Save all the parameters of the figure object into a dictionary
        :return: the dictionary with parameters
        """
        parameters = dict()
        parameters['fill_color'] = self.get_fill_color()
        parameters['outline_color'] = self.get_outline_color()
        parameters['outline_width'] = self.get_outline_width()
        parameters['start_x'] = self.__start_x
        parameters['start_y'] = self.__start_y
        parameters['figure_name'] = self.__name
        parameters['end_x'] = self.__end_x
        parameters['end_y'] = self.__end_y
        parameters['vertices_of_polygon'] = self.__vertices_of_polygon
        return parameters

    def add_to_canvas(self, canvas: tk.Canvas) -> None:
        """
        Adds the figure to the canvas according to the figure name
        :param canvas: a canvas which contains the figure object
        :return: None
        """
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
        """
        Moves the figure on canvas
        :param delta_x: change X axis position
        :param delta_y: change Y axis position
        :param canvas: a canvas which contains the figure object
        :return: None
        """
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
        """
        Returns the name of the figure
        :return: name of the figure from type string
        """
        return self.__name

    def add_vertex(self, vertex_x: float, vertex_y: float, canvas: tk.Canvas, replace_old: bool = False) -> None:
        """
        Adds a vertex to the polygon
        :param vertex_x: vertex x position
        :param vertex_y: vertex y position
        :param canvas: a canvas which contains the figure object
        :param replace_old: optional boolean parameter whether replace the previous vertex with a new one
        :return: None
        """
        if replace_old:
            self.__vertices_of_polygon[-1] = vertex_y
            self.__vertices_of_polygon[-2] = vertex_x
        else:
            self.__vertices_of_polygon.append(vertex_x)
            self.__vertices_of_polygon.append(vertex_y)
        self.redraw(canvas=canvas)

    def delete_last_vertex(self, canvas: tk.Canvas) -> None:
        """
        Deletes the last vertex of the polygon
        :param canvas: a canvas which contains the figure object
        :return: None
        """
        if len(self.__vertices_of_polygon) > 2:
            del self.__vertices_of_polygon[-1]
            del self.__vertices_of_polygon[-1]
            self.redraw(canvas=canvas)

    def delete_from_canvas(self, canvas: tk.Canvas) -> None:
        """
        Deletes the figure from canvas
        :param canvas: a canvas which contains the figure object
        :return: None
        """
        try:
            canvas.delete(self.id)
        except AttributeError:
            print("Object doesn't appear on canvas or canvas is not provided")

    def redraw(self, new_end_x: Any = None, new_end_y: Any = None, canvas: tk.Canvas = None) -> None:
        """
        Redraws the figure on canvas with new coordinates if figure is drawing
        :param new_end_x: optional new end x position of the figure
        :param new_end_y: optional new end y position of the figure
        :param canvas: a canvas which contains the figure object
        :return: None
        """
        if new_end_x is not None and new_end_y is not None:
            self.__end_x, self.__end_y = new_end_x, new_end_y
        self.delete_from_canvas(canvas=canvas)
        self.add_to_canvas(canvas=canvas)

    @staticmethod
    def load_from_dict(settings: dict) -> 'Figure':
        """
        Loads the figure from a dictionary settings and returns Figure object
        :param settings: dictionary with figure settings
        :return: object from Figure class
        """
        outline_color = settings['outline_color']
        outline_width = settings['outline_width']
        fill_color = settings['fill_color']
        start_x = settings['start_x']
        start_y = settings['start_y']
        end_x = settings['end_x']
        end_y = settings['end_y']
        figure_name = settings['figure_name']
        vertices_of_polygon = settings['vertices_of_polygon']
        return Figure(fill_color, outline_color, outline_width, start_x, figure_name, start_y, end_x,
                      vertices_of_polygon)
