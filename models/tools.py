from settings import (DEFAULT_BRUSH_SIZE, DEFAULT_BRUSH_COLOR, DEFAULT_TEXT_FONT,
                      DEFAULT_TEXT_SIZE, DEFAULT_TEXT_COLOR, LINE)


class BasicTool:
    """
    Class representing basic tool settings and function
    """

    def __init__(self, width: int = 5, color: str = 'black') -> None:
        """
        Initialize basic tool settings
        :param width: width of tool
        :param color: color of the tool on canvas
        :return: None
        """
        self.__width = width
        self.__color = color

    def change_tool_color(self, new_color: str = 'black') -> None:
        """
        Change old tool color to new one
        :param new_color: new color of the tool
        :return: None
        """
        self.__color = new_color

    def change_tool_width(self, new_width: int = 5) -> None:
        """
        Change old tool width to new one
        :param new_width: new width of the tool
        :return: None
        """
        self.__width = new_width

    def get_width(self) -> int:
        """
        Returns current width of the tool
        :return: a current width of the tool from type int
        """
        return self.__width

    def get_color(self) -> str:
        """
        Returns current color of the tool
        :return: a current color of the tool from type string
        """
        return self.__color


class Brush(BasicTool):
    """
    Class representing brush settings and functions
    """

    def __init__(self, width: int = DEFAULT_BRUSH_SIZE, color: str = DEFAULT_BRUSH_COLOR):
        """
        Initialize brush settings
        :param width: initial width of the brush
        :param color: initial color of the brush
        """
        super().__init__(width, color)


class Eraser(BasicTool):
    """
    Class representing eraser settings and functions
    """

    def __init__(self, width: int, color: str = 'white') -> None:
        """
        Initialize eraser settings
        :param width: initial width of the eraser
        :param color: initial color of the eraser
        """
        super().__init__(width, color)


class Texting:
    """
    Class representing text writing tool settings and functions
    """

    def __init__(self, font_family: str = DEFAULT_TEXT_FONT, font_size: int = DEFAULT_TEXT_SIZE,
                 font_color: str = DEFAULT_TEXT_COLOR) -> None:
        """
        Initialize text writing settings
        :param font_family: initial name of the font family
        :param font_size: initial font size
        :param font_color: initial font color
        """
        self.__font_family = font_family
        self.__font_size = font_size
        self.__font_color = font_color

    def get_font_family(self) -> str:
        """
        Returns current font family of the text writing tool
        :return: name of the font family from type string
        """
        return self.__font_family

    def get_font_size(self) -> int:
        """
        Returns current font size of the text writing tool
        :return: font size from type int
        """
        return self.__font_size

    def get_font_color(self) -> str:
        """
        Returns current font color of the text writing tool
        :return: font color from type string
        """
        return self.__font_color

    def change_font_family(self, new_font_family: str) -> None:
        """
        Changes the font family of the text writing tool
        :param new_font_family: name of the new font family
        :return: None
        """
        self.__font_family = new_font_family

    def change_font_size(self, new_font_size: int) -> None:
        """
        Changes the font size of the text writing tool
        :param new_font_size: new font size
        :return: None
        """
        self.__font_size = new_font_size

    def change_font_color(self, new_font_color: str) -> None:
        """
        Changes the font color of the text writing tool
        :param new_font_color: new font color
        :return: None
        """
        self.__font_color = new_font_color


class FigureDrawing:
    """
    Class representing figure drawing tool settings and functions
    """

    def __init__(self, fill_color: str = 'black', outline_color: str = 'black', outline_width: int = 5,
                 current_figure: str = LINE) -> None:
        """
        Initializes the figure drawing tool settings
        :param fill_color: initial fill color of the figure
        :param outline_color: initial outline color of the figure
        :param outline_width: initial outline width of the figure
        :param current_figure: name of the chosen figure type
        :return: None
        """
        self.__fill_color = fill_color
        self.__outline_color = outline_color
        self.__outline_width = outline_width
        self.__current_figure = current_figure

    def change_fill_color(self, new_color: str) -> None:
        """
        Changes the fill color of the figure drawing tool
        :param new_color: new fill color from type string
        :return: None
        """
        self.__fill_color = new_color

    def change_outline_color(self, new_color: str) -> None:
        """
        Changes the outline color of the figure drawing
        :param new_color: new outline color from type string
        :return: None
        """
        self.__outline_color = new_color

    def change_outline_width(self, new_width: int) -> None:
        """
        Changes the outline width of the figure drawing
        :param new_width: new outline width from type int
        :return: None
        """
        self.__outline_width = new_width

    def change_figure(self, new_figure: str) -> None:
        """
        Changes the figure to draw
        :param new_figure: name of the figure to draw
        :return: None
        """
        self.__current_figure = new_figure

    def get_current_figure(self) -> str:
        """
        Returns the current figure type
        :return: name of the current figure type
        """
        return self.__current_figure

    def get_outline_color(self) -> str:
        """
        Returns the outline color of the figure drawing tool
        :return: outline color of the tool from type string
        """
        return self.__outline_color

    def get_outline_width(self) -> int:
        """
        Returns the outline width of the figure drawing tool
        :return: outline width of the tool from type int
        """
        return self.__outline_width

    def get_fill_color(self) -> str:
        """
        Returns the fill color of the figure drawing tool
        :return: fill color of the tool from type string
        """
        return self.__fill_color