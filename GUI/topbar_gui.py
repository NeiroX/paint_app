import tkinter as tk
from GUI.bar_button import BarButton
from settings import BRUSH, ERASER, FIGURES, TEXT, SELECT, PRIMARY_COLOR, TOPBAR_HEIGHT, BUTTONS_PADDING, \
    DEFAULT_TEXT_FONT, FONT_FAMILIES, DEFAULT_BRUSH_SIZE, DEFAULT_BRUSH_COLOR


class TopBar(tk.Frame):
    """
    Frame for __topbar widgets. It's used to display all tools for change canvas tools and objects on top
    """

    def __init__(self, master=None, bg_color: str = PRIMARY_COLOR, height: int = TOPBAR_HEIGHT) -> None:
        # Constructor of topbar
        super().__init__(master, bg=bg_color, height=height)
        # Variable that tracks font family changing
        self.font_family = tk.StringVar(self, value=DEFAULT_TEXT_FONT)
        # Function that creates all widgets that might appear on topbar
        self._setup_buttons()

    def update_color_canvas_color(self, color: str) -> None:
        """
        Function to update outline color indicator
        :param color: color of canvas to indicate chosen outline color
        :return: None
        """
        self.color_canvas['bg'] = color

    def update_fill_canvas_color(self, color: str) -> None:
        """
        Function to change color of indicator that represents fill color of figure
        :param color: color of canvas to indicate chosen fill color
        :return: None
        """
        self.fill_canvas['bg'] = color

    def set_font_family(self, family: str) -> None:
        """
        Function to set font family of selected text area on cavnas
        :param family: name of font family
        :return: None
        """
        self.font_family.set(family)

    def get_font_family(self) -> str:
        """
        Function that returns the current chosen font family
        :return: string variable which contains font family name
        """
        return self.font_family.get()

    def _setup_buttons(self) -> None:
        """
        Function that creates all widgets for topbar.
        :return: None
        """
        # For brush
        self.color_button = BarButton(self, image_name='palette.png', text='outline_color')
        self.color_canvas = tk.Canvas(self, width=BUTTONS_PADDING * 10, height=TOPBAR_HEIGHT - 6 * BUTTONS_PADDING)

        # For figures
        self.fill_button = BarButton(self, image_name='fill.png', text='fill')
        self.fill_canvas = tk.Canvas(self, width=BUTTONS_PADDING * 10, height=TOPBAR_HEIGHT - 6 * BUTTONS_PADDING)
        self.line_button = BarButton(self, image_name='line.png', text='line')
        self.triangle_button = BarButton(self, image_name='triangle.png', text='triangle')
        self.oval_button = BarButton(self, image_name='oval.png', text='circle')
        self.rectangle_button = BarButton(self, image_name='rectangle.png', text='rectangle')
        self.polygon_button = BarButton(self, image_name='polygon.png', text='rectangle')

        # For brush, eraser, figures
        self.width_slider = tk.Scale(self, from_=1, to=100, orient=tk.HORIZONTAL, highlightthickness=0)
        self.width_slider.set(5)

        # For text
        self.font_family_list = tk.OptionMenu(self, self.font_family, *FONT_FAMILIES)

        # For select
        self.bring_forward_button = BarButton(self, image_name='bring-forward.png', text='bring forward',
                                              display_text=True)
        self.send_backward_button = BarButton(self, image_name='send-backward.png', text='send backward',
                                              display_text=True, compound=tk.RIGHT)
        self.remove_button = BarButton(self, image_name='remove.png', text='delete object', display_text=True)
        self.edit_text = BarButton(self, image_name='text-edit.png', text='edit text', display_text=True)
        self.remove_fill_button = BarButton(self, image_name='cross-circle.png', text='remove fill', display_text=True)

    def change_state(self, tool: str, width_value: int = 5, color_value: str = 'black',
                     fill_color_value: str = 'black', figures_on: bool = True,
                     font_family: str = DEFAULT_TEXT_FONT) -> None:
        """
        Function that changes topbar according to tool
        :param tool: name of the tool
        :param width_value: width value of brush, eraser and others from type int
        :param color_value: color value of brush, eraser and others from type str
        :param fill_color_value: color value for fill color of figure from type str
        :return: None
        """
        # Forget pack for select tool buttons
        self.bring_forward_button.pack_forget()
        self.send_backward_button.pack_forget()
        self.remove_button.pack_forget()
        self.edit_text.pack_forget()
        self.remove_fill_button.pack_forget()
        if tool == BRUSH:
            self._brush_state(width_value, color_value)
        elif tool == ERASER:
            self._eraser_state(width_value)
        elif tool == FIGURES:
            self._figures_state(width_value, color_value, fill_color_value, figures_on)
        elif tool == TEXT:
            self._text_state(width_value, color_value, font_family)
        elif tool == SELECT:
            self._select_state()

    def _brush_state(self, width_value: int = DEFAULT_BRUSH_SIZE, color_value: str = DEFAULT_BRUSH_COLOR) -> None:
        """
        Function to set the topbar widgets for brush tool
        :param width_value: thickness of brush from type int
        :param color_value: color of brush from type str
        :return: None
        """
        self.color_button.custom_pack(location=tk.LEFT)
        self.update_color_canvas_color(color_value)
        self.color_canvas.pack(padx=BUTTONS_PADDING, pady=BUTTONS_PADDING, side=tk.LEFT, fill=tk.BOTH)
        self.width_slider.set(width_value)
        self.width_slider.pack(side=tk.LEFT, pady=BUTTONS_PADDING, padx=BUTTONS_PADDING)
        self._forget_figures_buttons_pack()
        self.font_family_list.pack_forget()

    def _eraser_state(self, width_value: int = 5) -> None:
        """
        Function to set the topbar widgets for eraser tool
        :param width_value: thickness of eraser from type int
        :return: None
        """
        self.color_canvas.pack_forget()
        self.color_button.pack_forget()
        self.width_slider.set(width_value)
        self.width_slider.pack(side=tk.LEFT, pady=BUTTONS_PADDING, padx=BUTTONS_PADDING)
        self._forget_figures_buttons_pack()
        self.font_family_list.pack_forget()
        # self._forget_brush_buttons_pack()

    def _figures_state(self, width_value: int = 5, color_value: str = 'black', fill_color_value: str = 'black',
                       figures_on: bool = True) -> None:
        """
        Function to set the topbar widgets for figure creating tool
        :param width_value: thickness of outline from type int
        :param color_value: color of outline from type str
        :param fill_color_value: color of figure fill from type str
        :param figures_on:
        :return: None
        """
        self.color_button.custom_pack(location=tk.LEFT)
        self.update_color_canvas_color(color_value)
        self.color_canvas.pack(padx=BUTTONS_PADDING, pady=BUTTONS_PADDING, side=tk.LEFT, fill=tk.BOTH)
        self.update_fill_canvas_color(fill_color_value)
        self.width_slider.set(width_value)
        self.width_slider.pack(side=tk.LEFT, pady=BUTTONS_PADDING, padx=BUTTONS_PADDING)
        self._pack_figures_buttons(figures_on)
        self.font_family_list.pack_forget()
        # self._forget_brush_buttons_pack()

    def _text_state(self, width_value: int = 5, color_value: str = 'black',
                    font_family: str = DEFAULT_TEXT_FONT) -> None:
        """
        Function to set the topbar widgets for text writing tool
        :param width_value: size of text from type int
        :param color_value: color of font from type str
        :return:
        """
        self.update_color_canvas_color(color_value)
        self.color_canvas.pack(padx=BUTTONS_PADDING, pady=BUTTONS_PADDING, side=tk.LEFT, fill=tk.BOTH)
        self.fill_canvas.pack_forget()
        self.color_button.custom_pack(location=tk.LEFT)
        self.width_slider.set(width_value)
        self.width_slider.pack(side=tk.LEFT, pady=BUTTONS_PADDING, padx=BUTTONS_PADDING)
        self.set_font_family(font_family)
        self.font_family_list.pack(side=tk.LEFT, pady=BUTTONS_PADDING, padx=BUTTONS_PADDING)
        self._forget_figures_buttons_pack()
        # self._forget_brush_buttons_pack()

    def _select_state(self) -> None:
        """
        Function to set the topbar widgets for select tool
        :return: None
        """
        self.color_canvas.pack_forget()
        self.fill_canvas.pack_forget()
        self.color_button.pack_forget()
        self.width_slider.pack_forget()
        self.font_family_list.pack_forget()
        # self._forget_brush_buttons_pack()
        self._forget_figures_buttons_pack()

    def _forget_figures_buttons_pack(self) -> None:
        """
        Function to forget pack of some figures creating widgets
        :return: None
        """
        self.fill_canvas.pack_forget()
        self.fill_button.pack_forget()
        self.line_button.pack_forget()
        self.triangle_button.pack_forget()
        self.oval_button.pack_forget()
        self.rectangle_button.pack_forget()
        self.polygon_button.pack_forget()

    def _pack_figures_buttons(self, figures_on: bool) -> None:
        """
        Function to pack all figures creating widgets
        :return: None
        """
        self.fill_button.custom_pack(location=tk.LEFT)
        self.fill_canvas.pack(padx=BUTTONS_PADDING, pady=BUTTONS_PADDING, side=tk.LEFT, fill=tk.BOTH)
        if figures_on:
            self.line_button.custom_pack(location=tk.RIGHT)
            self.triangle_button.custom_pack(location=tk.RIGHT)
            self.oval_button.custom_pack(location=tk.RIGHT)
            self.rectangle_button.custom_pack(location=tk.RIGHT)
            self.polygon_button.custom_pack(location=tk.RIGHT)

    def custom_pack(self) -> None:
        """
        Custom packing of topbar widget on window
        :return: None
        """
        self.pack(side=tk.TOP, fill=tk.X)
