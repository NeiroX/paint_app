import tkinter as tk
from tkinter import colorchooser
import screeninfo
from typing import Any

from settings import *
from collections import deque
from models.drawing_classes import Line, Dot, Painted, TextArea
from models.tools import Brush, Eraser, Texting
from models.changes import BackgroundChange
from GUI.sidebar_gui import SideBar


class ApplicationGUI(tk.Tk):

    def __init__(self) -> None:

        # Creating window
        super().__init__()
        self.title("Paint")

        # Creating sidebar frame
        self.sidebar = SideBar(self, bg_color=PRIMARY_COLOR, width=SIDEBAR_WIDTH)
        self.sidebar.pack(side=tk.LEFT, fill=tk.BOTH)

        # Adapting window size to screen size
        self._set_application_window_size()
        # Setting up canvas
        self._setup_canvas()
        self.setup_commands()

        # Tools
        self._setup_tools()
        self.__current_tool = BRUSH

        # Stacks for changes in order to produce Undo and Redo functions
        self.__undo_stack = deque()
        self.__redo_stack = deque()

    def run(self) -> None:
        self.mainloop()

    def _setup_canvas(self):
        self.__canvas = tk.Canvas(self, bg=DEFAULT_CANVAS_COLOR, width=self.winfo_width(),
                                  height=self.winfo_height())
        self.__canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.__canvas.bind("<B1-Motion>", self._motion_dispatcher)
        self.__canvas.bind("<ButtonRelease-1>", self._reset)
        self.__canvas.bind("<Button-1>", self._click_dispatcher)
        self.start_x, self.start_y = None, None

    def _setup_tools(self):
        # Brush defining
        self.brush = Brush(width=5.0, color='black')
        # self.__current_painting = Line(self.brush.get_color(), self.brush.get_width())
        self.__current_painting = Painted()

        self.eraser = Eraser(width=5.0, color='white')
        self.texting = Texting()

    def _set_application_window_size(self) -> None:
        """
        Function that adapts the size of the window to the screen size
        :return:
        """
        try:
            screen_size = screeninfo.get_monitors()[0]
            screen_width = screen_size.width
            screen_height = screen_size.height
        except IndexError:
            print("Unable to get screen size. Width and height of window are set to default")
            screen_width = DEFAULT_SCREEN_WIDTH
            screen_height = DEFAULT_SCREEN_HEIGHT
        self.geometry(f"{screen_width}x{screen_height}")

    def setup_commands(self) -> None:
        self.sidebar.brush_button.set_command(self._use_brush)
        self.sidebar.eraser_button.set_command(self._use_eraser)
        self.sidebar.text_button.set_command(self._write_text)
        self.sidebar.figures_button.set_command(self._create_figure)
        self.sidebar.background_button.set_command(self._change_background_color)
        self.sidebar.trash_button.set_command(self._clear_all)
        self.sidebar.save_button.set_command(self._save)
        self.sidebar.select_button.set_command(self._use_select)
        self.sidebar.undo_button.set_command(self._undo)
        self.sidebar.redo_button.set_command(self._redo)
        self.sidebar.color_button.set_command(self._change_brush_color)

    def _use_brush(self) -> None:
        self.__current_tool = BRUSH

    def _use_eraser(self) -> None:
        self.__current_tool = ERASER

    def _write_text(self) -> None:
        self.__current_tool = TEXT

    def _use_select(self) -> None:
        self.__current_tool = SELECT

    def _create_figure(self) -> None:
        self.__current_tool = FIGURES

    def _change_background_color(self) -> None:
        selected_color = colorchooser.askcolor()[1]
        background_change = BackgroundChange(self.__canvas['bg'], selected_color)
        self.__undo_stack.append(background_change)
        self.__canvas['bg'] = selected_color
        self.sidebar.background_button['bg'] = selected_color

        print('Color changed')

    def _change_brush_color(self):
        selected_color = colorchooser.askcolor()[1]
        self.sidebar.color_button['bg'] = selected_color
        self.sidebar.color_button['fg'] = selected_color
        self.brush.change_brush_color(selected_color)
        print('Brush color changed')

    def _clear_all(self) -> None:
        self.__canvas.delete('all')
        self.__undo_stack.clear()
        self.__redo_stack.clear()
        self.sidebar.undo_button.disable()
        self.sidebar.redo_button.disable()
        self.__canvas['bg'] = DEFAULT_CANVAS_COLOR
        self.sidebar.background_button['bg'] = REGULAR_COLOR
        print('All cleared')

    def _save(self) -> None:
        image_file_name = 'result.png'
        path_to_save = os.path.join(BASE_DIR, image_file_name)
        self.__canvas.postscript(file=path_to_save, colormode='color')
        print('Image saved')

    def _motion_dispatcher(self, event: Any) -> None:
        x, y = event.x, event.y
        if self.__current_tool == BRUSH:
            self._paint(x, y)
        elif self.__current_tool == ERASER:
            self._erase(x, y)
        else:
            if not self.start_x and not self.start_y:
                self.start_x, self.start_y = x, y
            if self.__current_tool == FIGURES:
                self._create_figure(x, y)
            elif self.__current_tool == SELECT:
                self._select(x, y)

    def _create_figure(self, x, y):
        pass

    def _paint(self, x, y):
        new_dot = Dot((x, y), width=self.brush.get_width(), color=self.brush.get_color())
        new_dot.add_to_canvas(self.__canvas)
        self.__canvas.update()
        self.__current_painting.add_dot(new_dot)

    def _erase(self, x, y):
        items = self.__canvas.find_overlapping(x - self.eraser.get_width(), y - self.eraser.get_width(),
                                               x + self.eraser.get_width(),
                                               y + self.eraser.get_width())
        for item in items:
            # TODO: Add erased objects to undo_deque
            self.__canvas.delete(item)

    def _reset(self, event) -> None:
        if self.__current_tool == 'brush':
            self.start_x, self.start_y = None, None
            self.__undo_stack.append(self.__current_painting)
            self.sidebar.undo_button.enable()
            # self.__current_painting = Line(self.brush.get_color(), self.brush.get_width())
            self.__current_painting = Painted()

    def _undo(self) -> None:
        print(self.__undo_stack)
        if self.__undo_stack:
            last_change = self.__undo_stack.pop()
            self.__redo_stack.append(last_change)
            if type(last_change) is Painted:
                last_change.delete_from_canvas(self.__canvas)
            elif type(last_change) is BackgroundChange:
                self.__canvas['bg'] = last_change.get_previous_color()
            self.sidebar.redo_button.enable()
        if not self.__undo_stack:
            self.sidebar.undo_button.disable()

    def _redo(self) -> None:
        print(self.__redo_stack)
        if self.__redo_stack:
            last_undo = self.__redo_stack.pop()
            self.__undo_stack.append(last_undo)
            if type(last_undo) is Painted:
                last_undo.add_to_canvas(self.__canvas)
            elif type(last_undo) is BackgroundChange:
                self.__canvas['bg'] = last_undo.get_new_color()
            self.sidebar.undo_button.enable()
        if not self.__redo_stack:
            self.sidebar.redo_button.disable()

    def _click_dispatcher(self, event):
        x, y = event.x, event.y
        if self.__current_tool == TEXT:
            self._add_text(x, y)

    def _add_text(self, x, y):
        new_text = TextArea(x=x, y=y,
                            font_size=self.texting.get_font_size(),
                            font_color=self.texting.get_font_color(),
                            font_family=self.texting.get_font_family())
        # Ask user for text input
        new_text.change_text(self.__canvas)

    def _select(self, x, y):
        pass
