from tkinter import colorchooser
from GUI.canvas_panel import CanvasPanel
from models.changes import BackgroundChange
from settings import *
from models.drawing_classes import PaintGroup, Figure, Line, Paint, TextArea
from models.tools import Brush, Eraser, Texting, FigureDrawing
from collections import deque
from typing import Tuple, Any, Dict, Union


class CanvasManager:
    def __init__(self, canvas: CanvasPanel):
        self.__canvas = canvas
        self.__current_tool = BRUSH
        self.__paint_group_id = 1
        self.__current_painting = PaintGroup(self.__paint_group_id)
        self.__current_figure = None
        self.__selected_object = None
        self._setup_tools()

        # List of all objects
        self.__canvas_objects = list()
        # Stacks for changes in order to produce Undo and Redo functions
        self.__undo_stack = deque()
        self.__redo_stack = deque()
        self.start_x, self.start_y = None, None

    def _setup_tools(self):
        self.__brush = Brush(width=5, color='black')
        self.__eraser = Eraser(width=5, color='white')
        self.__texting = Texting()
        self.__figure_creating = FigureDrawing()

    def set_tool(self, tool: str) -> None:
        self.__current_tool = tool

    def paint(self, x: Any, y: Any):
        new_paint = Paint((x, y), width=self.__brush.get_width(), color=self.__brush.get_color())
        new_paint.add_to_canvas(self.__canvas)
        self.__canvas.update()
        self.__current_painting.add_paint(new_paint)

    def erase(self, x: Any, y: Any):
        if self.__eraser.is_remove_object():
            items = self.__canvas.find_overlapping(x - self.__eraser.get_width(), y - self.__eraser.get_width(),
                                                   x + self.__eraser.get_width(),
                                                   y + self.__eraser.get_width())
            for item in items:
                # TODO: Add erased objects to undo_deque
                for change in self.__undo_stack:
                    if type(change) is PaintGroup:
                        item_object = change.get_paint(item)
                        if change.remove_paint(item):
                            break
                self.__canvas.delete(item)

    def draw_figure(self, x: Any, y: Any):
        if self.start_x is None and self.start_y is None:
            self.start_x, self.start_y = x, y
        if self.__current_figure is not None:
            self.__current_figure.redraw(x, y, self.__canvas)
        elif self.__figure_creating.get_current_figure() == LINE:
            self.__current_figure = Line(start_x=self.start_x, start_y=self.start_y,
                                         outline_color=self.__figure_creating.get_outline_color(),
                                         outline_width=self.__figure_creating.get_outline_width())
            self.__current_figure.add_to_canvas(self.__canvas)
        else:
            self.__current_figure = Figure(start_x=self.start_x, start_y=self.start_y,
                                           fill_color=self.__figure_creating.get_fill_color(),
                                           outline_color=self.__figure_creating.get_outline_color(),
                                           outline_width=self.__figure_creating.get_outline_width(),
                                           figure_name=self.__figure_creating.get_current_figure())
            self.__current_figure.add_to_canvas(self.__canvas)

    def reset(self, x: Any, y: Any) -> None:
        self.start_x, self.start_y = None, None
        if self.__current_tool == BRUSH:
            self.__undo_stack.append(self.__current_painting)
            self.__canvas_objects.append(self.__current_painting)
            self.__paint_group_id += 1
            self.__current_painting = PaintGroup(self.__paint_group_id)
        elif self.__current_tool == FIGURES:
            self.__current_figure.redraw(x, y, self.__canvas)
            self.__undo_stack.append(self.__current_figure)
            self.__canvas_objects.append(self.__current_figure)
            self.__current_figure = None
        elif self.__current_tool == SELECT:
            self.__canvas_objects.append(self.__current_figure)
            self.__undo_stack.append(self.__current_figure)
            self.__selected_object = None

    def add_text(self, x: Any, y: Any):
        new_text = TextArea(x=x, y=y,
                            font_size=self.__texting.get_font_size(),
                            font_color=self.__texting.get_font_color(),
                            font_family=self.__texting.get_font_family())
        # Ask user for text input
        new_text.change_text(self.__canvas)
        self.__canvas_objects.append(new_text)
        self.__undo_stack.append(new_text)

    def select(self, x: Any, y: Any) -> Any:
        selected_object = self.__canvas.find_closest(x, y)
        if not selected_object:
            return None
        selected_object = selected_object[0]
        founded_object = None
        print(self.__canvas_objects)
        for obj in self.__canvas_objects:
            if type(obj) is PaintGroup:
                print('Search in PaintGroup')
                if selected_object in obj:
                    founded_object = obj
                    break
            elif type(obj) is Figure or type(obj) is Line or type(obj) is TextArea:
                if obj.id == selected_object:
                    founded_object = obj
                    break
        self.__selected_object = founded_object
        return type(founded_object)

    def move_selected(self, x: Any, y: Any) -> None:
        if not self.start_x and not self.start_y:
            self.start_x, self.start_y = x, y
        if self.__selected_object is not None:
            self.__selected_object.move(x - self.start_x, y - self.start_y, self.__canvas)
            self.start_x, self.start_y = x, y

    def set_line_figure(self) -> None:
        if self.__current_tool == FIGURES:
            self.__figure_creating.change_figure(LINE)

    def set_rectangle_figure(self) -> None:
        if self.__current_tool == FIGURES:
            self.__figure_creating.change_figure(RECTANGLE)

    def set_triangle_figure(self) -> None:
        if self.__current_tool == FIGURES:
            self.__figure_creating.change_figure(TRIANGLE)

    def set_oval_figure(self) -> None:
        if self.__current_tool == FIGURES:
            self.__figure_creating.change_figure(OVAL)

    def set_polygon_figure(self) -> None:
        if self.__current_tool == FIGURES:
            self.__figure_creating.change_figure(POLYGON)

    def get_figure_creating_parameters(self) -> Dict[str, Union[int, str]]:
        parameters = {
            'outline_color': self.__figure_creating.get_outline_color(),
            'outline_width': self.__figure_creating.get_outline_width(),
            'fill_color': self.__figure_creating.get_fill_color(),
            'figure': self.__figure_creating.get_current_figure()}
        return parameters

    def get_brush_parameters(self) -> Dict[str, Union[int, str]]:
        parameters = {'width': self.__brush.get_width(), 'color': self.__brush.get_color()}
        return parameters

    def set_brush_width(self, width: int) -> None:
        self.__brush.change_tool_width(width)

    def set_brush_color(self, color: str) -> None:
        self.__brush.change_tool_color(color)

    def set_eraser_width(self, width: int) -> None:
        self.__eraser.change_tool_width(width)

    def get_eraser_parameters(self) -> Dict[str, Union[int, str]]:
        parameters = {'width': self.__eraser.get_width()}
        return parameters

    def set_fill_color(self, color: str) -> None:
        self.__figure_creating.change_fill_color(color)

    def set_outline_color(self, color: str) -> None:
        self.__figure_creating.change_outline_color(color)

    def set_figure_name(self, name: str) -> None:
        self.__figure_creating.change_figure(name)

    def set_font_size(self, size: int) -> None:
        self.__texting.change_font_size(size)

    def set_font_color(self, color: str) -> None:
        self.__texting.change_font_color(color)

    def get_texting_parameters(self) -> Dict[str, Union[str, int]]:
        parameters = {'font_color': self.__texting.get_font_color(),
                      'font_size': self.__texting.get_font_size(),
                      'font_family': self.__texting.get_font_family()}
        return parameters

    def change_selected_fill_color(self, color: str) -> None:
        if self.__selected_object is not None:
            if type(self.__selected_object) is Figure:
                self.__selected_object.change_fill_color(color)
                self.__selected_object.redraw(canvas=self.__canvas)

    def change_selected_outline_color(self, color: str) -> None:
        if self.__selected_object is not None:
            if type(self.__selected_object) is Figure or type(self.__selected_object) is Line:
                self.__selected_object.change_outline_color(color)
                self.__selected_object.redraw(canvas=self.__canvas)
            elif type(self.__selected_object) is TextArea:
                self.__selected_object.change_font_color(color, self.__canvas)
            else:
                self.__selected_object.change_color(color, self.__canvas)

    def change_selected_width(self, width: int) -> None:
        if self.__selected_object is not None:
            if type(self.__selected_object) is Figure or type(self.__selected_object) is Line:
                self.__selected_object.change_outline_width(width)
                self.__selected_object.redraw(canvas=self.__canvas)
            elif type(self.__selected_object) is TextArea:
                self.__selected_object.change_font_size(width, self.__canvas)
            else:
                self.__selected_object.change_width(width, self.__canvas)

    def clear_all(self):
        self.__canvas.delete('all')
        self.__undo_stack.clear()
        self.__redo_stack.clear()
        self.__canvas_objects.clear()
        self.__canvas.reset_background_color()

    def save(self) -> None:
        image_file_name = 'result.jpg'
        path_to_save = os.path.join(BASE_DIR, image_file_name)
        self.__canvas.postscript(file=path_to_save, colormode='color')
        print('Image saved')

    def change_background_color(self) -> None:
        selected_color = colorchooser.askcolor()[-1]
        try:
            background_change = self.__canvas.change_background_color(selected_color)
            self.__undo_stack.append(background_change)
        except ValueError:
            print('Invalid background color. Please try again.')
            self.change_background_color()

    def undo(self) -> Tuple[bool, bool]:
        if self.__undo_stack:
            last_change = self.__undo_stack.pop()
            self.__redo_stack.append(last_change)
            if type(last_change) is PaintGroup:
                last_change.delete_from_canvas(self.__canvas)
            elif type(last_change) is BackgroundChange:
                self.__canvas['bg'] = last_change.get_previous_color()
            elif type(last_change) is Figure or type(last_change) is Line:
                last_change.delete_from_canvas(self.__canvas)
        return len(self.__undo_stack) > 0, len(self.__redo_stack) > 0

    def redo(self) -> Tuple[bool, bool]:
        if self.__redo_stack:
            last_undo = self.__redo_stack.pop()
            self.__undo_stack.append(last_undo)
            if type(last_undo) is PaintGroup:
                last_undo.add_to_canvas(self.__canvas)
            elif type(last_undo) is BackgroundChange:
                self.__canvas['bg'] = last_undo.get_new_color()
            elif type(last_undo) is Figure or type(last_undo) is Line:
                last_undo.add_to_canvas(self.__canvas)
        return len(self.__undo_stack) > 0, len(self.__redo_stack) > 0
