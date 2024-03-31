import tkinter as tk
from tkinter import colorchooser
import screeninfo
from typing import Any

from models.canvas_manager import CanvasManager
from settings import *
from collections import deque
from models.drawing_classes import PaintGroup, TextArea, Line, Figure
from models.tools import Brush, Eraser, Texting, FigureDrawing
from models.changes import BackgroundChange
from GUI.sidebar_gui import SideBar
from GUI.topbar_gui import TopBar
from GUI.canvas_panel import CanvasPanel


# TODO: create figures +-
# TODO: create magic selection +-
# TODO: add font changing variations +
# TODO: restructure of classes (create CanvasManager)
# TODO: create erasing not by object rather as brush
# TODO: create changes classes (ErasingChange, TextChange, MoveChange, FigureChange)
class ApplicationGUI(tk.Tk):

    def __init__(self) -> None:

        # Creating window
        super().__init__()
        self.title("Paint")

        # Creating sidebar frame
        self.sidebar = SideBar(self, bg_color=PRIMARY_COLOR, width=SIDEBAR_WIDTH)
        self.sidebar.custom_pack()

        # Creating __topbar frame
        self.__topbar = TopBar(self, bg_color=PRIMARY_COLOR, height=TOPBAR_HEIGHT)
        self.__topbar.custom_pack()

        # Adapting window size to screen size
        self._set_application_window_size()
        # Setting up canvas
        self._canvas = CanvasPanel(self, background_color=DEFAULT_CANVAS_COLOR, width=self.winfo_width(),
                                   height=self.winfo_height())
        self._canvas.custom_pack()
        self._canvas_manager = CanvasManager(canvas=self._canvas)
        self._setup_binds()
        self.setup_commands()

        # Tools
        self.__current_tool = BRUSH
        self.start_x, self.start_y = None, None
        self.__topbar.change_state(BRUSH)

        # Stacks for changes in order to produce Undo and Redo functions
        self.__undo_stack = deque()
        self.__redo_stack = deque()

    def run(self) -> None:
        self.mainloop()

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
        self.sidebar.background_button.set_command(self._canvas_manager.change_background_color)
        self.sidebar.trash_button.set_command(self._clear_all)
        self.sidebar.save_button.set_command(self._canvas_manager.save)
        self.sidebar.select_button.set_command(self._use_select)
        self.sidebar.undo_button.set_command(self._undo)
        self.sidebar.redo_button.set_command(self._redo)
        self.__topbar.color_button.set_command(self._change_outline_color)
        self.__topbar.width_slider.configure(command=self._change_tool_width)
        self.__topbar.line_button.set_command(self._canvas_manager.set_line_figure)
        self.__topbar.triangle_button.set_command(self._canvas_manager.set_triangle_figure)
        self.__topbar.polygon_button.set_command(self._canvas_manager.set_polygon_figure)
        self.__topbar.rectangle_button.set_command(self._canvas_manager.set_rectangle_figure)
        self.__topbar.oval_button.set_command(self._canvas_manager.set_oval_figure)
        self.__topbar.fill_button.set_command(self._change_fill_color)

    def _use_brush(self) -> None:
        self.__current_tool = BRUSH
        self._canvas_manager.set_tool(BRUSH)
        parameters = self._canvas_manager.get_brush_parameters()
        self.__topbar.change_state(BRUSH, width_value=parameters['width'],
                                   color_value=parameters['color'])

    def _use_eraser(self) -> None:
        self.__current_tool = ERASER
        self._canvas_manager.set_tool(ERASER)
        parameters = self._canvas_manager.get_eraser_parameters()
        self.__topbar.change_state(ERASER, width_value=parameters['width'])

    def _write_text(self) -> None:
        self.__current_tool = TEXT
        self._canvas_manager.set_tool(TEXT)
        parameters = self._canvas_manager.get_texting_parameters()
        self.__topbar.change_state(TEXT, width_value=parameters['font_size'], color_value=parameters['font_color'])
        self.__topbar.set_font_family(parameters['font_family'])

    def _use_select(self) -> None:
        self.__current_tool = SELECT
        self._canvas_manager.set_tool(SELECT)
        self.__topbar.change_state(SELECT)

    def _create_figure(self) -> None:
        self.__current_tool = FIGURES
        self._canvas_manager.set_tool(FIGURES)
        parameters = self._canvas_manager.get_figure_creating_parameters()
        self.__topbar.change_state(FIGURES, width_value=parameters['outline_width'],
                                   fill_color_value=parameters['fill_color'],
                                   color_value=parameters['outline_color'])

    def _change_outline_color(self) -> None:
        new_color = colorchooser.askcolor()[1]
        self.__topbar.update_color_canvas_color(new_color)
        if self.__current_tool == BRUSH:
            self._canvas_manager.set_brush_color(new_color)
            print('Brush outline_color changed')
        elif self.__current_tool == FIGURES:
            self._canvas_manager.set_outline_color(new_color)
        elif self.__current_tool == TEXT:
            self._canvas_manager.set_font_color(new_color)
        elif self.__current_tool == SELECT:
            self._canvas_manager.change_selected_outline_color(new_color)

    def _change_fill_color(self) -> None:
        new_color = colorchooser.askcolor()[1]
        self.__topbar.update_fill_canvas_color(new_color)
        if self.__current_tool == FIGURES:
            self._canvas_manager.set_fill_color(new_color)
        elif self.__current_tool == SELECT:
            self._canvas_manager.change_selected_fill_color(new_color)

    def _setup_binds(self) -> None:
        self._canvas.bind("<B1-Motion>", self._motion_dispatcher)
        self._canvas.bind("<ButtonRelease-1>", self._reset)
        self._canvas.bind("<Button-1>", self._click_dispatcher)

    def _change_tool_width(self, event) -> None:
        new_width = self.__topbar.width_slider.get()
        if self.__current_tool == BRUSH:
            self._canvas_manager.set_brush_width(new_width)
        elif self.__current_tool == ERASER:
            self._canvas_manager.set_eraser_width(new_width)
        elif self.__current_tool == TEXT:
            self._canvas_manager.set_font_size(new_width)
        elif self.__current_tool == SELECT:
            self._canvas_manager.change_selected_width(new_width)

    def _clear_all(self) -> None:
        self._canvas_manager.clear_all()
        self.sidebar.undo_button.is_enabled(False)
        self.sidebar.redo_button.is_enabled(False)

    def _motion_dispatcher(self, event: Any) -> None:
        x, y = event.x, event.y
        if self.__current_tool == BRUSH:
            self._canvas_manager.paint(x, y)
        elif self.__current_tool == ERASER:
            self._canvas_manager.erase(event.x, event.y)
        elif self.__current_tool == FIGURES:
            self._canvas_manager.draw_figure(event.x, event.y)
        elif self.__current_tool == SELECT:
            self._canvas_manager.move_selected(event.x, event.y)

    def _reset(self, event) -> None:
        self._canvas_manager.reset(event.x, event.y)
        if self.__current_tool in [BRUSH, FIGURES]:
            self.sidebar.undo_button.is_enabled(True)
        elif self.__current_tool == SELECT:
            self.__topbar.change_state(SELECT)

    def _do_buttons_enable_status(self, is_undo_enabled: bool, is_redo_enabled: bool) -> None:
        self.sidebar.undo_button.is_enabled(is_undo_enabled)
        self.sidebar.redo_button.is_enabled(is_redo_enabled)

    def _undo(self) -> None:
        is_undo_enabled, is_redo_enabled = self._canvas_manager.undo()
        self._do_buttons_enable_status(is_undo_enabled, is_redo_enabled)

    def _redo(self) -> None:
        is_undo_enabled, is_redo_enabled = self._canvas_manager.redo()
        self._do_buttons_enable_status(is_undo_enabled, is_redo_enabled)

    def _click_dispatcher(self, event):
        x, y = event.x, event.y
        if self.__current_tool == TEXT:
            self._canvas_manager.add_text(x, y)
        elif self.__current_tool == SELECT:
            selected_type = self._canvas_manager.select(x, y)
            self._adapt_topbar_to_select(selected_type)

    def _adapt_topbar_to_select(self, selected_type):
        if selected_type is TextArea:
            self.__topbar.change_state(TEXT)
        elif selected_type is PaintGroup:
            self.__topbar.change_state(BRUSH)
        elif selected_type is Figure or selected_type is Line:
            self.__topbar.change_state(FIGURES)
