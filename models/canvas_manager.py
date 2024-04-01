from tkinter import colorchooser
from GUI.canvas_panel import CanvasPanel
from settings import *
from models.changes import BackgroundChange, DeleteObjectChange, SelectedChange
from models.draw_objects import PaintGroup, Figure, Line, Paint, TextArea
from models.tools import Brush, Eraser, Texting, FigureDrawing
from collections import deque
from typing import Tuple, Any, Dict, Union, Optional


class CanvasManager:
    """
    Manages the canvas objects and draws custom objects according to the chosen tool
    """

    def __init__(self, canvas: CanvasPanel, project: Dict[str, Any] = None) -> None:
        """
        Initializes manager variables such as tools, stacks for redo and undo actions, empty canvas objects
        :param canvas: canvas to manage
        """
        self.__canvas = canvas
        self.__current_tool = BRUSH
        self.__paint_group_id = 1
        self.__current_painting = PaintGroup(self.__paint_group_id)
        self.__current_figure = None
        self.__selected_object = None

        # Setting up all tools
        self._setup_tools()

        # List of all objects
        self.__canvas_objects = list()
        # Stacks for changes in order to produce Undo and Redo functions
        self.__undo_stack = deque()
        self.__redo_stack = deque()
        self.start_x, self.start_y = None, None
        if project is not None:
            self._load_canvas_from_dict(project)

    def _setup_tools(self) -> None:
        """
        Function that sets up tools
        :return: None
        """
        self.__brush = Brush(width=5, color='black')
        self.__eraser = Eraser(width=5, color='white')
        self.__texting = Texting()
        self.__figure_creating = FigureDrawing()

    def set_tool(self, tool: str) -> None:
        """
        Choosing tool depending on the buttons on sidebar
        :param tool: name of the tool
        :return: None
        """
        self.__current_tool = tool
        self.end_drawing_polygon()

    def paint(self, x: Any, y: Any) -> None:
        """
        Function to paint on canvas
        :param x: event x position
        :param y: event y position
        :return: None
        """
        # Creating dot on canvas
        new_paint = Paint((x, y), width=self.__brush.get_width(), color=self.__brush.get_color())
        new_paint.add_to_canvas(self.__canvas)
        self.__canvas.update()
        # Adding dot to the group
        self.__current_painting.add_paint(new_paint)

    def paint_on_click(self, x: Any, y: Any) -> None:
        """
        Function to paint on canvas on click
        :param x: event x position
        :param y: event y position
        :return: None
        """
        new_paint = Paint((x, y), width=self.__brush.get_width(), color=self.__brush.get_color())
        new_paint.add_to_canvas(self.__canvas)
        self.__canvas.update()
        self.__current_painting.add_paint(new_paint)
        self.__undo_stack.append(self.__current_painting)
        self.__canvas_objects.append(self.__current_painting)
        self.__paint_group_id += 1
        self.__current_painting = PaintGroup(self.__paint_group_id)

    def erase(self, x: Any, y: Any) -> None:
        """
        Erasing objects on canvas
        :param x: event x position
        :param y: event y position
        :return: None
        """
        # Searching for the objects according to given x, y positions and eraser width
        items = self.__canvas.find_overlapping(x - self.__eraser.get_width(), y - self.__eraser.get_width(),
                                               x + self.__eraser.get_width(),
                                               y + self.__eraser.get_width())
        # Saving changes to stack and deleting object
        for item in items:
            new_delete_change = None
            for canvas_object in self.__canvas_objects:
                if type(canvas_object) is PaintGroup:
                    item_object = canvas_object.get_paint(item)
                    if item is not None:
                        self.__canvas_objects.remove(canvas_object)
                        canvas_object.remove_paint(item)
                        new_delete_change = DeleteObjectChange(item_object, canvas_object)
                        self.__canvas_objects.append(canvas_object)
                        break
                elif canvas_object.id == item:
                    new_delete_change = DeleteObjectChange(canvas_object)
                    self.__canvas_objects.remove(canvas_object)
                    break
            if new_delete_change is not None:
                self.__undo_stack.append(new_delete_change)
            self.__canvas.delete(item)

    def draw_polygon(self, x: Any, y: Any) -> None:
        """
        Updates polygon while user's drawing
        :param x: event x position
        :param y: event y position
        :return: None
        """
        if self.__current_tool == FIGURES and self.__figure_creating.get_current_figure() == POLYGON:
            if self.__current_figure is not None:
                self.__current_figure.add_vertex(x, y, self.__canvas, replace_old=True)

    def add_vertex_to_polygon(self, x: Any, y: Any) -> None:
        """
        Adds a new vertex information to the polygon verteces list
        :param x: event x position
        :param y: event y position
        :return: None
        """
        if self.__current_tool == FIGURES and self.__figure_creating.get_current_figure() == POLYGON:
            if self.__current_figure is not None:
                self.__current_figure.add_vertex(x, y, self.__canvas, replace_old=True)
            else:
                self.__current_figure = Figure(start_x=x,
                                               start_y=y,
                                               outline_color=self.__figure_creating.get_outline_color(),
                                               fill_color=self.__figure_creating.get_fill_color(),
                                               outline_width=self.__figure_creating.get_outline_width(),
                                               figure_name=self.__figure_creating.get_current_figure())

    def end_drawing_polygon(self) -> None:
        """
        Function that saves polygon and ends its drawing after RMB click
        :return:
        """
        if self.__current_figure is not None and self.__current_figure.get_figure_name() == POLYGON:
            self.__current_figure.delete_last_vertex(self.__canvas)
            self.__undo_stack.append(self.__current_figure)
            self.__canvas_objects.append(self.__current_figure)
            self.__current_figure = None

    def draw_figure(self, x: Any, y: Any) -> None:
        """
        Drawing figure on canvas according to the chosen figure type in figure creating tool
        :param x: event x position
        :param y: event y position
        :return: None
        """
        # Setting start coordinates
        if self.start_x is None and self.start_y is None and self.__current_figure is None:
            self.start_x, self.start_y = x, y
        # Update figure while creating
        if self.__current_figure is not None and self.__figure_creating.get_current_figure() != POLYGON:
            self.__current_figure.redraw(x, y, self.__canvas)
        # Creating figures
        elif self.__figure_creating.get_current_figure() == LINE:
            # Line with outline parameter only
            self.__current_figure = Line(start_x=self.start_x, start_y=self.start_y,
                                         outline_color=self.__figure_creating.get_outline_color(),
                                         outline_width=self.__figure_creating.get_outline_width())
            self.__current_figure.add_to_canvas(self.__canvas)
        elif self.__figure_creating.get_current_figure() != POLYGON:
            # Figure with fill parameter
            self.__current_figure = Figure(start_x=self.start_x, start_y=self.start_y,
                                           fill_color=self.__figure_creating.get_fill_color(),
                                           outline_color=self.__figure_creating.get_outline_color(),
                                           outline_width=self.__figure_creating.get_outline_width(),
                                           figure_name=self.__figure_creating.get_current_figure())
            self.__current_figure.add_to_canvas(self.__canvas)

    def _clear_redo_stack(self) -> None:
        """
        Clears the redo stack when new change are done if undo stack is not empty
        :return: None
        """
        pass
        if self.__redo_stack and self.__undo_stack:
            self.__redo_stack.clear()

    def reset(self, x: Any, y: Any) -> None:
        """
        Function that Rrsets the mouse drag and save changes on canvas
        :param x: event x position
        :param y: event y postion
        :return: None
        """
        self.start_x, self.start_y = None, None
        self._clear_redo_stack()
        if self.__current_tool == BRUSH:
            self.__undo_stack.append(self.__current_painting)
            self.__canvas_objects.append(self.__current_painting)
            self.__paint_group_id += 1
            self.__current_painting = PaintGroup(self.__paint_group_id)
        elif self.__current_tool == FIGURES:
            if self.__figure_creating.get_current_figure() != POLYGON:
                if self.__current_figure is not None:
                    self.__current_figure.redraw(x, y, self.__canvas)
                    self.__undo_stack.append(self.__current_figure)
                    self.__canvas_objects.append(self.__current_figure)
                self.__current_figure = None
            else:
                self.__current_figure.add_vertex(x, y, self.__canvas)

    def add_text(self, x: Any, y: Any) -> None:
        """
        Function that adds text to the canvas in chosen position.
        Parameters of text are set according to text writing tool.
        :param x: event x position
        :param y: event y position
        :return: None
        """
        new_text = TextArea(x=x, y=y,
                            font_size=self.__texting.get_font_size(),
                            font_color=self.__texting.get_font_color(),
                            font_family=self.__texting.get_font_family())
        # Ask user for text input via dialog window
        new_text.change_text(self.__canvas)
        self.__canvas_objects.append(new_text)
        self._clear_redo_stack()
        self.__undo_stack.append(new_text)

    def _make_copy_of_selected(self):
        """
        Function that makes a copy of the selected object and adds changes on selected object to undo stack
        :return: None
        """
        old_copy = self.__selected_object
        self.__selected_object = old_copy.copy()
        self._delete_object_from_canvas(old_copy)
        self.__canvas_objects.append(self.__selected_object)
        self.__undo_stack.append(SelectedChange(old_copy, self.__selected_object))

    def edit_selected_text(self) -> Optional[bool]:
        """
        Function that calls text editing for the selected text object
        :return: boolean result of text editing
        """
        if self.__current_tool == SELECT:
            if self.__selected_object is not None:
                self._make_copy_of_selected()
                self.__selected_object.change_text(self.__canvas)
                return True

    def remove_fill_color(self) -> Optional[bool]:
        """
        Function that removes the fill color of the selected figure
        :return: boolean result of removing fill color
        """
        if self.__current_tool == SELECT:
            if self.__selected_object is not None:
                self._make_copy_of_selected()
                self.__selected_object.change_fill_color(None)
                self.__selected_object.redraw(canvas=self.__canvas)
                return True

    def select(self, x: Any, y: Any) -> Any:
        """
        Function that search object on canvas
        :param x: event x position
        :param y: event y position
        :return: selected object or None
        """
        selected_object = self.__canvas.find_overlapping(x - DEFAULT_BRUSH_SIZE, y - DEFAULT_BRUSH_SIZE,
                                                         x + DEFAULT_BRUSH_SIZE, y + DEFAULT_BRUSH_SIZE)
        if not selected_object:
            return None
        selected_object = selected_object[0]
        founded_object = None
        # Define custom object type
        for obj in self.__canvas_objects:
            if type(obj) is PaintGroup:
                if selected_object in obj:
                    founded_object = obj
                    break
            elif type(obj) is Figure or type(obj) is Line or type(obj) is TextArea:
                if obj.id == selected_object:
                    founded_object = obj
                    break
        self.__selected_object = founded_object
        return founded_object

    def move_selected(self, x: Any, y: Any) -> None:
        """
        Function that moves selected object with mouse
        :param x: event x position
        :param y: event y position
        :return: None
        """
        if not self.start_x and not self.start_y:
            self.start_x, self.start_y = x, y
            if self.__selected_object:
                self._clear_redo_stack()
                self._make_copy_of_selected()
        if self.__selected_object is not None:
            self.__selected_object.move(x - self.start_x, y - self.start_y, self.__canvas)
            self.start_x, self.start_y = x, y

    def bring_forward(self) -> None:
        """
        Function that brings selected object to forward layer according to selected object type
        :return: None
        """
        if self.__selected_object is not None:
            self._clear_redo_stack()
            self._make_copy_of_selected()
            selected_object_type = type(self.__selected_object)
            if selected_object_type == PaintGroup:
                self.__selected_object.bring_forward(self.__canvas)
            elif selected_object_type is Figure or selected_object_type is Line or selected_object_type is TextArea:
                self.__canvas.tag_raise(self.__selected_object.id)

    def send_backward(self) -> None:
        """
        Function that sends selected object to backward layer according to selected object type
        :return: None
        """
        if self.__selected_object is not None:
            self._clear_redo_stack()
            self._make_copy_of_selected()
            selected_object_type = type(self.__selected_object)
            if selected_object_type == PaintGroup:
                self.__selected_object.send_backward(self.__canvas)
            elif selected_object_type is Figure or selected_object_type is Line or selected_object_type is TextArea:
                self.__canvas.tag_lower(self.__selected_object.id)

    def remove_object(self) -> None:
        """
        Function that removes selected object from canvas and saves changes to stack
        :return: None
        """
        if self.__selected_object is not None:
            selected_object_type = type(self.__selected_object)
            if selected_object_type == PaintGroup:
                self.__selected_object.delete_from_canvas(self.__canvas)
            elif selected_object_type is Figure or selected_object_type is Line:
                self.__selected_object.delete_from_canvas(self.__canvas)
            elif selected_object_type is TextArea:
                self.__canvas.delete(self.__selected_object.id)
            self.__undo_stack.append(DeleteObjectChange(self.__selected_object))
            self.__selected_object = None

    def set_line_figure(self) -> None:
        """
        Function that sets line as figure to create
        :return: None
        """
        if self.__current_tool == FIGURES:
            self.__figure_creating.change_figure(LINE)
            self.end_drawing_polygon()

    def set_rectangle_figure(self) -> None:
        """
        Function that sets rectangle as figure to create
        :return: None
        """
        if self.__current_tool == FIGURES:
            self.__figure_creating.change_figure(RECTANGLE)
            self.end_drawing_polygon()

    def set_triangle_figure(self) -> None:
        """
        Function that sets triangle as figure to create
        :return: None
        """
        if self.__current_tool == FIGURES:
            self.__figure_creating.change_figure(TRIANGLE)
            self.end_drawing_polygon()

    def set_oval_figure(self) -> None:
        """
        Function that sets oval as figure to create
        :return: None
        """
        if self.__current_tool == FIGURES:
            self.__figure_creating.change_figure(OVAL)
            self.end_drawing_polygon()

    def set_polygon_figure(self) -> None:
        """
        Function that sets polygon as figure to create
        :return: None
        """
        if self.__current_tool == FIGURES:
            self.__figure_creating.change_figure(POLYGON)
            self.end_drawing_polygon()

    def get_figure_creating_parameters(self) -> Dict[str, Union[int, str]]:
        """
        Function that returns the figure creating settings for GUI widgets
        :return parameters: dictionary with settings
        """
        parameters = {
            'outline_color': self.__figure_creating.get_outline_color(),
            'outline_width': self.__figure_creating.get_outline_width(),
            'fill_color': self.__figure_creating.get_fill_color(),
            'figure': self.__figure_creating.get_current_figure()}
        return parameters

    def get_brush_parameters(self) -> Dict[str, Union[int, str]]:
        """
        Function that returns brush settings for GUI widgets
        :return parameters: dictionary with settings
        """
        parameters = {'width': self.__brush.get_width(), 'color': self.__brush.get_color()}
        return parameters

    def set_brush_width(self, width: int) -> None:
        """
        Function that sets the width of the brush tool
        :param width: a width of brush from type int
        :return: None
        """
        self.__brush.change_tool_width(width)

    def set_brush_color(self, color: str) -> None:
        """
        Function that sets the color of the brush tool
        :param color: a color of brush from type string
        :return: None
        """
        self.__brush.change_tool_color(color)

    def set_eraser_width(self, width: int) -> None:
        """
        Function that sets the width of the eraser tool
        :param width: a width of eraser from type int
        :return: None
        """
        self.__eraser.change_tool_width(width)

    def get_eraser_parameters(self) -> Dict[str, Union[int, str]]:
        """
        Function that returns the settings of the eraser tool for GUI widgets.
        :return parameters: a dictionary of settings
        """
        parameters = {'width': self.__eraser.get_width()}
        return parameters

    def set_fill_color(self, color: str) -> None:
        """
        Function that sets the color of the figure fill
        :param color: a color for filling from type string
        :return: None
        """
        self.__figure_creating.change_fill_color(color)
        self.end_drawing_polygon()

    def set_outline_color(self, color: str) -> None:
        """
        Function that sets the color of the outline for figure creating tool
        :param color: a color of outline from type string
        :return: None
        """
        self.__figure_creating.change_outline_color(color)
        self.end_drawing_polygon()

    def set_outline_width(self, width: int) -> None:
        """
        Function that sets the width of the outline for figure creating tool
        :param width: a width of outline from type int
        :return: None
        """
        self.__figure_creating.change_outline_width(width)
        self.end_drawing_polygon()

    def set_font_size(self, size: int) -> None:
        """
        Function that sets the font size for text writing tool
        :param size: a font size from type int
        :return:
        """
        self.__texting.change_font_size(size)

    def set_font_color(self, color: str) -> None:
        """
        Function that sets the font color for text writing tool
        :param color: a color of font from type string
        :return: None
        """
        self.__texting.change_font_color(color)

    def set_font_family(self, family: str) -> None:
        """
        Function that sets the font family for text writing or for selected_object
        :param family: a font family name from type string
        :return: None
        """
        if self.__current_tool == TEXT:
            self.__texting.change_font_family(family)
        elif self.__current_tool == SELECT:
            if self.__selected_object is not None:
                self._make_copy_of_selected()
                self.__selected_object.change_font_family(family, self.__canvas)

    def get_texting_parameters(self) -> Dict[str, Union[str, int]]:
        """
        Function that returns the settings of the text writing tool for GUI widgets
        :return parameters: a dictionary of settings
        """
        parameters = {'font_color': self.__texting.get_font_color(),
                      'font_size': self.__texting.get_font_size(),
                      'font_family': self.__texting.get_font_family()}
        return parameters

    def change_selected_fill_color(self, color: Optional[str]) -> None:
        """
        Function that sets the fill color for selected figure
        :param color: a color for filling selected figure
        :return: None
        """
        if self.__selected_object is not None:
            self._clear_redo_stack()
            self._make_copy_of_selected()
            if type(self.__selected_object) is Figure:
                self.__selected_object.change_fill_color(color)
                self.__selected_object.redraw(canvas=self.__canvas)

    def change_selected_outline_color(self, color: str) -> None:
        """
        Function that sets the outline color for selected object
        :param color: a color for outline of selected object
        :return: None
        """
        if self.__selected_object is not None:
            self._clear_redo_stack()
            self._make_copy_of_selected()
            if type(self.__selected_object) is Figure or type(self.__selected_object) is Line:
                self.__selected_object.change_outline_color(color)
                self.__selected_object.redraw(canvas=self.__canvas)
            elif type(self.__selected_object) is TextArea:
                self.__selected_object.change_font_color(color, self.__canvas)
            else:
                self.__selected_object.change_color(color, self.__canvas)

    def change_selected_width(self, width: int) -> None:
        """
        Function that sets the width of outline for selected object
        :param width: a width of outline for selected object
        :return: None
        """
        if self.__selected_object is not None:
            self._clear_redo_stack()
            self._make_copy_of_selected()
            if type(self.__selected_object) is Figure or type(self.__selected_object) is Line:
                self.__selected_object.change_outline_width(width)
                self.__selected_object.redraw(canvas=self.__canvas)
            elif type(self.__selected_object) is TextArea:
                self.__selected_object.change_font_size(width, self.__canvas)
            else:
                self.__selected_object.change_width(width, self.__canvas)

    def clear_all(self) -> None:
        """
        Function that clears all objects from canvas and clears stacks and list of objects, reset canvas background
        :return: None
        """
        self.end_drawing_polygon()
        self.__canvas.delete('all')
        self.__undo_stack.clear()
        self.__redo_stack.clear()
        self.__canvas_objects.clear()
        self.__canvas.reset_background_color()

    def save_as_image(self) -> None:
        """
        Function that saves current canvas to image file
        :return: None
        """
        self.end_drawing_polygon()
        self.__canvas.save()

    def save_canvas_to_dict(self) -> Dict[Any, Any]:
        """
        Function that saves current canvas to dictionary
        :return: a dictionary which contains all objects on canvas
        """
        canvas_dict = dict()
        canvas_dict['PaintGroup'] = list()
        canvas_dict['Line'] = list()
        canvas_dict['Figure'] = list()
        canvas_dict['TextArea'] = list()
        canvas_dict['canvas_color'] = self.__canvas.get_background_color()
        for obj in self.__canvas_objects:
            if type(obj) is PaintGroup:
                canvas_dict['PaintGroup'].append(obj.save_settings_to_dict())
            elif type(obj) is Figure:
                canvas_dict['Figure'].append(obj.save_settings_to_dict())
            elif type(obj) is Line:
                canvas_dict['Line'].append(obj.save_settings_to_dict())
            elif type(obj) is TextArea:
                canvas_dict['TextArea'].append(obj.save_settings_to_dict())

        return canvas_dict

    def _load_canvas_from_dict(self, canvas_dict: Dict[Any, Any]) -> None:
        """
        Load canvas from given dictionary and update the variables
        :param canvas_dict: canvas settings
        :return: None
        """
        self.__canvas.change_background_color(canvas_dict['canvas_color'])
        paint_groups = canvas_dict['PaintGroup']
        for group in paint_groups:
            self.__paint_group_id = group['id']
            new_group = PaintGroup.load_from_dict(group)
            self.__canvas_objects.append(new_group)
            new_group.add_to_canvas(self.__canvas)
        for line in canvas_dict['Line']:
            new_line = Line.load_from_dict(line)
            self.__canvas_objects.append(new_line)
            new_line.add_to_canvas(self.__canvas)
        for figure in canvas_dict['Figure']:
            new_figure = Figure.load_from_dict(figure)
            self.__canvas_objects.append(new_figure)
            new_figure.add_to_canvas(self.__canvas)
        for text in canvas_dict['TextArea']:
            new_text = TextArea.load_from_dict(text)
            self.__canvas_objects.append(new_text)
            new_text.add_to_canvas(self.__canvas)
        self.__canvas.update()

    def change_background_color(self) -> None:
        """
        Function that changes background color of canvas
        :return: None
        """
        self.end_drawing_polygon()
        selected_color = colorchooser.askcolor()[-1]
        try:
            background_change = self.__canvas.change_background_color(selected_color)
            self._clear_redo_stack()
            self.__undo_stack.append(background_change)
        except ValueError:
            print('Invalid background color. Please try again.')
            self.change_background_color()

    def undo(self) -> Tuple[bool, bool]:
        """
        Function that undoes the previous action
        :return bool, bool: True if stack is empty, False otherwise
        """
        self.end_drawing_polygon()
        if self.__undo_stack:
            last_change = self.__undo_stack.pop()
            self.__redo_stack.append(last_change)
            if type(last_change) in [PaintGroup, Figure, Line, TextArea]:
                self._delete_object_from_canvas(last_change)
            elif type(last_change) is BackgroundChange:
                self.__canvas.change_background_color(last_change.get_previous_color())
            elif type(last_change) is DeleteObjectChange:
                object_to_add, paint_group = last_change.get_deleted_object()
                self._add_object_to_canvas(object_to_add)
                if paint_group is not None:
                    paint_group.add_paint(object_to_add)
            elif type(last_change) is SelectedChange:
                old_object, new_object = last_change.get_change()
                self._delete_object_from_canvas(new_object)
                self._add_object_to_canvas(old_object)
        return len(self.__undo_stack) > 0, len(self.__redo_stack) > 0

    def redo(self) -> Tuple[bool, bool]:
        """
        Function that redoes the previous undone action
        :return bool, bool: True if stack is empty, False otherwise
        """
        self.end_drawing_polygon()
        if self.__redo_stack:
            last_undo = self.__redo_stack.pop()
            self.__undo_stack.append(last_undo)
            if type(last_undo) in [PaintGroup, Figure, Line, TextArea]:
                self._add_object_to_canvas(last_undo)
            elif type(last_undo) is BackgroundChange:
                self.__canvas.change_background_color(last_undo.get_new_color())
            elif type(last_undo) is DeleteObjectChange:
                object_to_delete, paint_group = last_undo.get_deleted_object()
                self._delete_object_from_canvas(object_to_delete)
                if paint_group is not None:
                    paint_group.remove_paint(object_to_delete.id)
            elif type(last_undo) is SelectedChange:
                old_object, new_object = last_undo.get_change()
                self._delete_object_from_canvas(old_object)
                self._add_object_to_canvas(new_object)
        return len(self.__undo_stack) > 0, len(self.__redo_stack) > 0

    def _delete_object_from_canvas(self, object_to_delete: Any) -> None:
        """
        Function that deletes back the given object from the canvas
        :param object_to_delete: object to delete
        :return: None
        """
        if type(object_to_delete) in [Paint, TextArea]:
            self.__canvas.delete(object_to_delete.id)
        elif object_to_delete is not None:
            object_to_delete.delete_from_canvas(self.__canvas)
        if type(object_to_delete) is not Paint:
            try:
                self.__canvas_objects.remove(object_to_delete)
            except ValueError:
                print('Object is not on canvas')

    def _add_object_to_canvas(self, object_to_add: Any) -> None:
        """
        Function that adds back the given object to the canvas
        :param object_to_add: object to add
        :return: None
        """
        if object_to_add is not None:
            object_to_add.add_to_canvas(self.__canvas)
        if type(object_to_add) is not Paint:
            self.__canvas_objects.append(object_to_add)
