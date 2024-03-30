import tkinter as tk
from GUI.application_gui import ApplicationGUI
from settings import *
from models.tools import Brush, Eraser, Texting
from models.drawing_classes import Painted, Dot, TextArea


class PaintingController:
    def __init__(self):
        # Creating
        self._app_gui = ApplicationGUI()
        self._current_tool = BRUSH
        self._setup_tools()

    def run(self):
        self._app_gui.run()

    def _setup_tools(self):
        # Brush definition
        self.brush = Brush(width=5.0, color='black')
        # self.__current_painting = Line(self.brush.get_color(), self.brush.get_width())
        self.__current_painting = Painted()

        # Eraser definition
        self.eraser = Eraser(width=5.0, color='white')
        # Texting definition
        self.texting = Texting()

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
