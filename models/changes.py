from typing import Any, Tuple
import tkinter as tk
from models.draw_objects import PaintGroup, Paint, TextArea, Line, Figure


class BackgroundChange:
    """
    Class representing a canvas background change
    """

    def __init__(self, previous_color: str, new_color: str) -> None:
        self.__previous_color = previous_color
        self.__new_color = new_color

    def get_previous_color(self) -> str:
        return self.__previous_color

    def get_new_color(self) -> str:
        return self.__new_color


class SelectedChange:
    def __init__(self, previous_object: Any, new_object: Any) -> None:
        self.__old_object = previous_object
        self.__new_object = new_object

    def get_change(self) -> Tuple[Any, Any]:
        return self.__old_object, self.__new_object


class DeleteObjectChange:
    def __init__(self, deleted_object: Any, paint_group: PaintGroup = None) -> None:
        self.__deleted_object = deleted_object
        self.__paint_group = paint_group

    def get_deleted_object(self) -> Any:
        return self.__deleted_object, self.__paint_group

