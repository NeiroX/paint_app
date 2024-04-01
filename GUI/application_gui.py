import tkinter as tk
from tkinter import colorchooser
import screeninfo
from typing import Any

from models.canvas_manager import CanvasManager
from models.project import Project
from settings import *
from models.draw_objects import PaintGroup, TextArea, Line, Figure
from GUI.sidebar_gui import SideBar
from GUI.topbar_gui import TopBar
from GUI.canvas_panel import CanvasPanel


class ApplicationGUI(tk.Tk):
    """
    Main application window that wires the canvas logic and other GUI functionality. It inherits from tkinter.Tk
    """

    def __init__(self) -> None:
        """
        Initializes the application window with all necessary widgets on it
        """

        # Creating window
        super().__init__()
        self.title("Paint")

        # Creating __sidebar frame
        self.__sidebar = SideBar(self, bg_color=PRIMARY_COLOR, width=SIDEBAR_WIDTH)
        self.__sidebar.custom_pack()

        # Creating __topbar frame
        self.__topbar = TopBar(self, bg_color=PRIMARY_COLOR, height=TOPBAR_HEIGHT)
        self.__topbar.custom_pack()

        # Adapting window size to screen size
        self._set_application_window_size()
        # Setting up canvas
        self._canvas = CanvasPanel(self, background_color=DEFAULT_CANVAS_COLOR, width=self.winfo_width(),
                                   height=self.winfo_height())
        self._canvas.custom_pack()
        self._project = Project(PROJECT_FILE_NAME)
        self._canvas_manager = CanvasManager(canvas=self._canvas, project=self._project.open())
        self._setup_binds()

        # Setting up commands for sidebar and topbar buttons
        self._setup_commands()

        # Tools
        self.__current_tool = BRUSH
        self.start_x, self.start_y = None, None
        self.__topbar.change_state(BRUSH)

    def run(self) -> None:
        """
        Starts the application window and starts the GUI loop
        :return: None
        """
        self.mainloop()

    def _set_application_window_size(self) -> None:
        """
        Function that adapts the size of the window to the screen size
        :return: None
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

    def _setup_binds(self) -> None:
        """
        Function that sets up the binds for the application canvas
        :return: None
        """
        self._canvas.bind("<B1-Motion>", self._drag_dispatcher)
        self._canvas.bind("<ButtonRelease-1>", self._reset)
        self._canvas.bind("<Button-1>", self._click_dispatcher)
        self._canvas.bind("<Motion>", self._motion_dispatcher)
        self._canvas.bind("<Button-2>", self._second_mouse_button_dispatcher)

    def _setup_commands(self) -> None:
        """
        Function that sets up commands for the sidebar and topbar widgets and wires it to canvas logic
        :return: None
        """
        self.__sidebar.brush_button.set_command(self._use_brush)
        self.__sidebar.eraser_button.set_command(self._use_eraser)
        self.__sidebar.text_button.set_command(self._write_text)
        self.__sidebar.figures_button.set_command(self._create_figure)
        self.__sidebar.background_button.set_command(self._canvas_manager.change_background_color)
        self.__sidebar.clear_button.set_command(self._clear_all)
        self.__sidebar.save_button.set_command(self._canvas_manager.save_as_image)
        self.__sidebar.select_button.set_command(self._use_select)
        self.__sidebar.undo_button.set_command(self._undo)
        self.__sidebar.redo_button.set_command(self._redo)
        self.__sidebar.close_app_button.set_command(self._save_project)
        self.__topbar.color_button.set_command(self._change_outline_color)
        self.__topbar.width_slider.configure(command=self._change_tool_width)
        self.__topbar.line_button.set_command(self._canvas_manager.set_line_figure)
        self.__topbar.triangle_button.set_command(self._canvas_manager.set_triangle_figure)
        self.__topbar.polygon_button.set_command(self._canvas_manager.set_polygon_figure)
        self.__topbar.rectangle_button.set_command(self._canvas_manager.set_rectangle_figure)
        self.__topbar.oval_button.set_command(self._canvas_manager.set_oval_figure)
        self.__topbar.fill_button.set_command(self._change_fill_color)
        self.__topbar.font_family.trace('w', self._change_font_family)
        self.__topbar.bring_forward_button.set_command(self._canvas_manager.bring_forward)
        self.__topbar.send_backward_button.set_command(self._canvas_manager.send_backward)
        self.__topbar.remove_button.set_command(self._canvas_manager.remove_object)
        self.__topbar.edit_text.set_command(self._edit_text)
        self.__topbar.remove_fill_button.set_command(self._remove_fill)

    def _save_project(self) -> None:
        """
        Save the current project to json file and close app window
        :return: None
        """
        saved_canvas = self._canvas_manager.save_canvas_to_dict()
        self._project.save(saved_canvas)
        # Clothing window
        self.destroy()

    def _disable_redo_button(self) -> None:
        """
        Disable redo button after change if undo stack is not empty
        :return: None
        """
        if self.__sidebar.redo_button.get_state() and self.__sidebar.undo_button.get_state():
            self.__sidebar.redo_button.is_enabled(False)

    def _use_brush(self) -> None:
        """
        Changing tool to brush and changing appearance of topbar
        :return: None
        """
        self.__current_tool = BRUSH
        self._canvas_manager.set_tool(BRUSH)
        parameters = self._canvas_manager.get_brush_parameters()
        self.__topbar.change_state(BRUSH, width_value=parameters['width'],
                                   color_value=parameters['color'])

    def _use_eraser(self) -> None:
        """
        Changing tool to eraser and changing appearance of topbar
        :return: None
        """
        self.__current_tool = ERASER
        self._canvas_manager.set_tool(ERASER)
        parameters = self._canvas_manager.get_eraser_parameters()
        self.__topbar.change_state(ERASER, width_value=parameters['width'])

    def _write_text(self) -> None:
        """
        Changing tool to text writing tool and changing appearance of topbar
        :return: None
        """
        self.__current_tool = TEXT
        self._canvas_manager.set_tool(TEXT)
        parameters = self._canvas_manager.get_texting_parameters()
        self.__topbar.change_state(TEXT, width_value=parameters['font_size'], color_value=parameters['font_color'])
        self.__topbar.set_font_family(parameters['font_family'])

    def _use_select(self) -> None:
        """
        Changing tool to select tool and changing appearance of topbar
        :return: None
        """
        self.__current_tool = SELECT
        self._canvas_manager.set_tool(SELECT)
        self.__topbar.change_state(SELECT)

    def _create_figure(self) -> None:
        """
        Changing tool to figure creating and changing appearance of topbar
        :return: None
        """
        self.__current_tool = FIGURES
        self._canvas_manager.set_tool(FIGURES)
        parameters = self._canvas_manager.get_figure_creating_parameters()
        self.__topbar.change_state(FIGURES, width_value=parameters['outline_width'],
                                   fill_color_value=parameters['fill_color'],
                                   color_value=parameters['outline_color'])

    def _change_outline_color(self) -> None:
        """
        Calling dialog window to choose outline color and then change outline color according to chosen tool
        :return: None
        """
        try:
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
        except IndexError:
            print('The color is not choosed, please, try again')
            self._change_outline_color()

    def _change_fill_color(self) -> None:
        """
        Calling dialog window to choose fill color and then change fill color according to chosen tool
        :return: None
        """
        try:
            new_color = colorchooser.askcolor()[1]
            self.__topbar.update_fill_canvas_color(new_color)
            if self.__current_tool == FIGURES:
                self._canvas_manager.set_fill_color(new_color)
            elif self.__current_tool == SELECT:
                self._canvas_manager.change_selected_fill_color(new_color)
        except IndexError:
            print('The color is not choosed, please, try again')
            self._change_fill_color()

    def _change_tool_width(self, event: Any) -> None:
        """
        Getting current width according to topbar widget and setting the width according to chosen tool
        :param event: event data
        :return: None
        """
        new_width = self.__topbar.width_slider.get()
        if self.__current_tool == BRUSH:
            self._canvas_manager.set_brush_width(new_width)
        elif self.__current_tool == ERASER:
            self._canvas_manager.set_eraser_width(new_width)
        elif self.__current_tool == TEXT:
            self._canvas_manager.set_font_size(new_width)
        elif self.__current_tool == SELECT:
            self._canvas_manager.change_selected_width(new_width)

    def _change_font_family(self, *args) -> None:
        """
        Changing font family for text writing tool
        :param args: arguments for function
        :return: None
        """
        self._canvas_manager.set_font_family(self.__topbar.get_font_family())
        if self.__current_tool == SELECT:
            self._disable_redo_button()
            self.__sidebar.undo_button.is_enabled(True)

    def _edit_text(self) -> None:
        """
        Function that edits text for selected text object
        :return: None
        """
        if self.__current_tool == SELECT:
            result = self._canvas_manager.edit_selected_text()
            self._disable_redo_button()
            if result is not None:
                self.__sidebar.undo_button.is_enabled(result)

    def _remove_fill(self) -> None:
        """
        Function that removes fill color for selected figure
        :return: None
        """
        if self.__current_tool == SELECT:
            result = self._canvas_manager.remove_fill_color()
            self._disable_redo_button()
            if result is not None:
                self.__sidebar.undo_button.is_enabled(result)

    def _clear_all(self) -> None:
        """
        Clear canvas and delete all objects. Disable undo and redo buttons on sidebar
        :return: None
        """
        self._canvas_manager.clear_all()
        self.__sidebar.undo_button.is_enabled(False)
        self.__sidebar.redo_button.is_enabled(False)

    def _motion_dispatcher(self, event: Any) -> None:
        """
        Dispatcher for mouse motion on canvas
        :param event: event information
        :return: None
        """
        if self.__current_tool == FIGURES:
            self._canvas_manager.draw_polygon(event.x, event.y)

    def _second_mouse_button_dispatcher(self, event: Any) -> None:
        """
        Dispatcher for right mouse click
        :param event: event information
        :return: None
        """
        if self.__current_tool == FIGURES:
            self._canvas_manager.end_drawing_polygon()
            self._disable_redo_button()
            self.__sidebar.undo_button.is_enabled(True)

    def _drag_dispatcher(self, event: Any) -> None:
        """
        Dispatcher for mouse drag events
        :param event: event information
        :return: None
        """
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
        """
        Reset mouse drag and add final result to canvas
        :param event: event information
        :return: None
        """
        self._canvas_manager.reset(event.x, event.y)
        if self.__current_tool in [BRUSH, FIGURES]:
            self.__sidebar.undo_button.is_enabled(True)
            self._disable_redo_button()
        # elif self.__current_tool == SELECT:
        # self.__topbar.change_state(SELECT)

    def _do_buttons_enable_status(self, is_undo_enabled: bool, is_redo_enabled: bool) -> None:
        """
        Local function to make undo and redo buttons enabled or disabled depending on content of canvas
        :param is_undo_enabled: boolean variable representing whether undo button is enabled
        :param is_redo_enabled: boolean variable representing whether redo button is enabled
        :return: None
        """
        self.__sidebar.undo_button.is_enabled(is_undo_enabled)
        self.__sidebar.redo_button.is_enabled(is_redo_enabled)

    def _undo(self) -> None:
        """
        Undo function and changing enable state for undo and redo buttons
        :return: None
        """
        is_undo_enabled, is_redo_enabled = self._canvas_manager.undo()
        self._do_buttons_enable_status(is_undo_enabled, is_redo_enabled)
        if self.__current_tool == SELECT:
            self.__topbar.change_state(SELECT)

    def _redo(self) -> None:
        """
        Redo function and changing enable state for undo and redo buttons
        :return: None
        """
        is_undo_enabled, is_redo_enabled = self._canvas_manager.redo()
        self._do_buttons_enable_status(is_undo_enabled, is_redo_enabled)
        if self.__current_tool == SELECT:
            self.__topbar.change_state(SELECT)

    def _click_dispatcher(self, event: Any) -> None:
        """
        Dispatcher for mouse click events
        :param event: event information
        :return: None
        """
        x, y = event.x, event.y
        # if self.__current_tool == BRUSH:
        #     self._canvas_manager.paint_on_click(x, y)
        if self.__current_tool == FIGURES:
            self._canvas_manager.add_vertex_to_polygon(x, y)
            return
        if self.__current_tool == TEXT:
            self._canvas_manager.add_text(x, y)
            self.__sidebar.undo_button.is_enabled(True)
        elif self.__current_tool == SELECT:
            selected_object = self._canvas_manager.select(x, y)
            self._adapt_topbar_to_select(selected_object)
        self._disable_redo_button()

    def _adapt_topbar_to_select(self, selected_object: Any) -> None:
        """
        Adapt topbar to selected object
        :param selected_object: a selected object
        :return: None
        """
        selected_type = type(selected_object)
        print(selected_type)
        if selected_type is TextArea:
            self.__topbar.change_state(TEXT,
                                       width_value=selected_object.get_font_size(),
                                       color_value=selected_object.get_font_color(),
                                       font_family=selected_object.get_font_family())
            self.__topbar.edit_text.custom_pack(location=tk.LEFT)
        elif selected_type is PaintGroup:
            self.__topbar.change_state(BRUSH,
                                       color_value=selected_object.get_color(),
                                       width_value=selected_object.get_width())
        elif selected_type is Figure or selected_type is Line:
            fill_color = selected_object.get_fill_color() if selected_type is not Line else 'black'
            self.__topbar.change_state(FIGURES, figures_on=False,
                                       width_value=selected_object.get_outline_width(),
                                       color_value=selected_object.get_outline_color(),
                                       fill_color_value=fill_color)
            self.__topbar.remove_fill_button.custom_pack(location=tk.LEFT)
        if selected_type is not None:
            self.__topbar.bring_forward_button.custom_pack(location=tk.LEFT)
            self.__topbar.send_backward_button.custom_pack(location=tk.LEFT)
            self.__topbar.remove_button.custom_pack(location=tk.LEFT)
        else:
            self.__topbar.change_state(SELECT)
