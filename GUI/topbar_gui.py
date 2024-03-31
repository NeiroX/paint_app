import tkinter as tk
from GUI.bar_button import BarButton
from settings import BRUSH, ERASER, FIGURES, TEXT, SELECT, PRIMARY_COLOR, TOPBAR_HEIGHT, BUTTONS_PADDING, \
    DEFAULT_TEXT_FONT, FONT_FAMILIES, DEFAULT_BRUSH_SIZE, DEFAULT_BRUSH_COLOR


class TopBar(tk.Frame):
    def __init__(self, master=None, bg_color: str = PRIMARY_COLOR, height: int = TOPBAR_HEIGHT) -> None:
        super().__init__(master, bg=bg_color, height=height)
        self.__font_family = tk.StringVar(self, value=DEFAULT_TEXT_FONT)
        self._setup_buttons()

    def update_color_canvas_color(self, color: str) -> None:
        self.color_canvas['bg'] = color

    def update_fill_canvas_color(self, color: str) -> None:
        self.fill_canvas['bg'] = color

    def set_font_family(self, family: str) -> None:
        self.__font_family.set(family)

    def get_font_family(self) -> str:
        return self.__font_family.get()

    def _setup_buttons(self):
        # For brush
        self.color_button = BarButton(self, image_name='palette.png', text='outline_color')
        # TODO: add color_canvas to text and text outline_color choosing button
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
        self.font_family_button = tk.OptionMenu(self, variable=self.__font_family, value=FONT_FAMILIES)

    def change_state(self, tool: str, width_value: int = 5, color_value: str = 'black',
                     fill_color_value: str = 'black') -> None:
        if tool == BRUSH:
            self._brush_state(width_value, color_value)
        elif tool == ERASER:
            self._eraser_state(width_value)
        elif tool == FIGURES:
            self._figures_state(width_value, color_value, fill_color_value)
        elif tool == TEXT:
            self._text_state(width_value)
        elif tool == SELECT:
            self._select_state()

    def _brush_state(self, width_value: int = DEFAULT_BRUSH_SIZE, color_value: str = DEFAULT_BRUSH_COLOR) -> None:
        self.color_button.custom_pack(location=tk.LEFT)
        self.update_color_canvas_color(color_value)
        self.color_canvas.pack(padx=BUTTONS_PADDING, pady=BUTTONS_PADDING, side=tk.LEFT, fill=tk.BOTH)
        self.width_slider.set(width_value)
        self.width_slider.pack(side=tk.LEFT, pady=BUTTONS_PADDING, padx=BUTTONS_PADDING)
        self._forget_figures_buttons_pack()
        self.font_family_button.pack_forget()

    def _eraser_state(self, width_value: int = 5) -> None:
        self.color_canvas.pack_forget()
        self.color_button.pack_forget()
        self.width_slider.set(width_value)
        self.width_slider.pack(side=tk.LEFT, pady=BUTTONS_PADDING, padx=BUTTONS_PADDING)
        self._forget_figures_buttons_pack()
        self.font_family_button.pack_forget()
        # self._forget_brush_buttons_pack()

    def _figures_state(self, width_value: int = 5, color_value: str = 'black', fill_color_value: str = 'black') -> None:
        self.color_button.custom_pack(location=tk.LEFT)
        self.update_color_canvas_color(color_value)
        self.color_canvas.pack(padx=BUTTONS_PADDING, pady=BUTTONS_PADDING, side=tk.LEFT, fill=tk.BOTH)
        self.update_fill_canvas_color(fill_color_value)
        self.width_slider.set(width_value)
        self.width_slider.pack(side=tk.LEFT, pady=BUTTONS_PADDING, padx=BUTTONS_PADDING)
        self._pack_figures_buttons()
        self.font_family_button.pack_forget()
        # self._forget_brush_buttons_pack()

    def _text_state(self, width_value: int = 5, color_value: str = 'black') -> None:
        self.update_color_canvas_color(color_value)
        self.color_canvas.pack(padx=BUTTONS_PADDING, pady=BUTTONS_PADDING, side=tk.LEFT, fill=tk.BOTH)
        self.fill_canvas.pack_forget()
        self.color_button.custom_pack(location=tk.LEFT)
        self.width_slider.set(width_value)
        self.width_slider.pack(side=tk.LEFT, pady=BUTTONS_PADDING, padx=BUTTONS_PADDING)
        self.font_family_button.pack(side=tk.LEFT, pady=BUTTONS_PADDING, padx=BUTTONS_PADDING)
        self._forget_figures_buttons_pack()
        # self._forget_brush_buttons_pack()

    def _select_state(self) -> None:
        self.color_canvas.pack_forget()
        self.fill_canvas.pack_forget()
        self.color_button.pack_forget()
        self.width_slider.pack_forget()
        self.font_family_button.pack_forget()
        # self._forget_brush_buttons_pack()
        self._forget_figures_buttons_pack()

    def _forget_figures_buttons_pack(self):
        self.fill_canvas.pack_forget()
        self.fill_button.pack_forget()
        self.line_button.pack_forget()
        self.triangle_button.pack_forget()
        self.oval_button.pack_forget()
        self.rectangle_button.pack_forget()
        self.polygon_button.pack_forget()

    def _pack_figures_buttons(self):
        self.fill_button.custom_pack(location=tk.LEFT)
        self.fill_canvas.pack(padx=BUTTONS_PADDING, pady=BUTTONS_PADDING, side=tk.LEFT, fill=tk.BOTH)
        self.line_button.custom_pack(location=tk.RIGHT)
        self.triangle_button.custom_pack(location=tk.RIGHT)
        self.oval_button.custom_pack(location=tk.RIGHT)
        self.rectangle_button.custom_pack(location=tk.RIGHT)
        self.polygon_button.custom_pack(location=tk.RIGHT)

    def custom_pack(self):
        self.pack(side=tk.TOP, fill=tk.X)
