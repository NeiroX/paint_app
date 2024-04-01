from typing import Any, Tuple, Optional
import tkinter as tk
from models.draw_objects import PaintGroup, Paint, TextArea, Line, Figure


class BackgroundChange:
    """
    Class representing a canvas background change
    """

    def __init__(self, previous_color: str, new_color: str) -> None:
        """
        Initializes a background change
        :param previous_color: a previous color of the canvas background from type string
        :param new_color: a new color of the canvas background from type string
        """
        self.__previous_color = previous_color
        self.__new_color = new_color

    def get_previous_color(self) -> str:
        """
        Returns the previous color of the canvas background after performed change
        :return: a previous color from type string
        """
        return self.__previous_color

    def get_new_color(self) -> str:
        """
        Returns the new color of the canvas background after performed change
        :return: a new color from type string
        """
        return self.__new_color


class SelectedChange:
    """
    Class representing a performed change on selected object. It contains old and new versions of objects
    """
    def __init__(self, old_object: Any, new_object: Any) -> None:
        """
        Initializes a change on selected object
        :param old_object: an old version of the selected object
        :param new_object: a new version of the selected object
        """
        self.__old_object = old_object
        self.__new_object = new_object

    def get_change(self) -> Tuple[Any, Any]:
        """
        Returns the old and new versions of the selected object
        :return: tuple that contains objects of old and new versions of the selected object
        """
        return self.__old_object, self.__new_object


class DeleteObjectChange:
    """
    Class representing a performed delete change on object
    """
    def __init__(self, deleted_object: Any, paint_group: PaintGroup = None) -> None:
        """
        Initializes a performed delete change
        :param deleted_object: removed object
        :param paint_group: optional parameter used to add back Paint to Paint Group
        """
        self.__deleted_object = deleted_object
        self.__paint_group = paint_group

    def get_deleted_object(self) -> Tuple[Any, Optional[PaintGroup]]:
        """
        Returns the deleted object and paint group if it exists
        :return: tuple that contains deleted object and paint group if it exists, otherwise None
        """
        return self.__deleted_object, self.__paint_group

