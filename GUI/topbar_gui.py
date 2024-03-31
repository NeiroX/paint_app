import tkinter as tk
from GUI.bar_button import BarButton
from settings import BRUSH, ERASER, FIGURES, TEXT, SELECT, PRIMARY_COLOR, TOPBAR_HEIGHT, BUTTONS_PADDING


class TopBar(tk.Frame):
    def __init__(self, master=None, bg_color: str = PRIMARY_COLOR, height: int = TOPBAR_HEIGHT) -> None:
        super().__init__(master, bg=bg_color, height=height)
        self._setup_buttons()

    def update_color_canvas_color(self, color: str) -> None:
        self.color_canvas['bg'] = color

    def _setup_buttons(self):
        # For brush
        self.color_button = BarButton(self, image_name='palette.png', text='color')
        # TODO: add color_canvas to text and text color choosing button
        self.color_canvas = tk.Canvas(self, width=BUTTONS_PADDING * 10, height=TOPBAR_HEIGHT - 6 * BUTTONS_PADDING)

        self.dot_style = BarButton(self, image_name='', text='brush dot', display_text=True)
        self.line_style = BarButton(self, image_name='', text='brush line', display_text=True)
        self.polygon_style = BarButton(self, image_name='', text='brush polygon', display_text=True)

        # For figures
        self.fill_button = BarButton(self, image_name='palette.png', text='fill')
        self.outline_color_button = BarButton(self, text='outline color')
        self.triangle_button = BarButton(self, image_name='triangle.png', text='triangle')
        self.oval_button = BarButton(self, image_name='oval.png', text='circle')
        self.rectangle_button = BarButton(self, image_name='rectangle.png', text='rectangle')

        # For brush, eraser, figures
        # self.width_button = BarButton(self, image_name='line-width.png', text='width')
        self.width_slider = tk.Scale(self, from_=1, to=100, orient=tk.HORIZONTAL, highlightthickness=0)
        self.width_slider.set(5)

        # For text
        self.font_family_button = BarButton(self, text='font family')
        self.font_color_button = BarButton(self, text='font color')
        # self.font_size_button = BarButton(self, image_name='text-size.png', text='font size')

    def change_state(self, tool: str, width_value: int = None, color_value: str = None) -> None:
        if tool == BRUSH:
            self._brush_state(width_value, color_value)
        elif tool == ERASER:
            self._eraser_state(width_value)
        elif tool == FIGURES:
            self._figures_state(width_value, color_value)
        elif tool == TEXT:
            self._text_state(width_value)
        elif tool == SELECT:
            self._select_state()

    def _brush_state(self, width_value: int = 5, color_value: str = 'black') -> None:
        # self.color_button.change_button_color(color_value)
        self.color_button.custom_pack(location=tk.LEFT)
        self.update_color_canvas_color(color_value)
        self.color_canvas.pack(padx=BUTTONS_PADDING, pady=BUTTONS_PADDING, side=tk.LEFT, fill=tk.BOTH)
        self.width_slider.set(width_value)
        self.width_slider.pack(side=tk.LEFT, pady=BUTTONS_PADDING, padx=BUTTONS_PADDING)
        self._forget_figures_buttons_pack()
        self._forget_text_buttons_pack()
        self._pack_brush_buttons()

    def _eraser_state(self, width_value: int = 5) -> None:
        self.color_canvas.pack_forget()
        self.color_button.pack_forget()
        self.width_slider.set(width_value)
        self.width_slider.pack(side=tk.LEFT, pady=BUTTONS_PADDING, padx=BUTTONS_PADDING)
        self._forget_figures_buttons_pack()
        self._forget_text_buttons_pack()
        self._forget_brush_buttons_pack()

    def _figures_state(self, width_value: int = 5, color_value: str = 'black') -> None:
        self.update_color_canvas_color(color_value)
        self.color_canvas.pack(padx=BUTTONS_PADDING, pady=BUTTONS_PADDING, side=tk.LEFT, fill=tk.BOTH)
        self.width_slider.set(width_value)
        self.width_slider.pack(side=tk.LEFT, pady=BUTTONS_PADDING, padx=BUTTONS_PADDING)
        self._pack_figures_buttons()
        self._forget_text_buttons_pack()
        self._forget_brush_buttons_pack()

    def _text_state(self, width_value: int = 5) -> None:
        self.color_canvas.pack_forget()
        self.color_button.pack_forget()
        self.width_slider.set(width_value)
        self.width_slider.pack(side=tk.LEFT, pady=BUTTONS_PADDING, padx=BUTTONS_PADDING)
        self._pack_text_buttons()
        self._forget_figures_buttons_pack()
        self._forget_brush_buttons_pack()

    def _select_state(self) -> None:
        self.color_canvas.pack_forget()
        self.color_button.pack_forget()
        self.width_slider.pack_forget()
        self._forget_text_buttons_pack()
        self._forget_figures_buttons_pack()
        self._forget_brush_buttons_pack()

    def _forget_figures_buttons_pack(self):
        self.outline_color_button.pack_forget()
        self.fill_button.pack_forget()
        self.triangle_button.pack_forget()
        self.oval_button.pack_forget()
        self.rectangle_button.pack_forget()

    def _pack_figures_buttons(self):
        self.outline_color_button.custom_pack(location=tk.LEFT)
        self.fill_button.custom_pack(location=tk.LEFT)
        self.triangle_button.custom_pack(location=tk.RIGHT)
        self.oval_button.custom_pack(location=tk.RIGHT)
        self.rectangle_button.custom_pack(location=tk.RIGHT)

    def _forget_text_buttons_pack(self):
        self.font_color_button.pack_forget()
        self.font_family_button.pack_forget()

    def _pack_text_buttons(self):
        self.font_color_button.custom_pack(location=tk.LEFT)
        self.font_family_button.custom_pack(location=tk.LEFT)

    def _forget_brush_buttons_pack(self):
        self.dot_style.pack_forget()
        self.line_style.pack_forget()
        self.polygon_style.pack_forget()

    def _pack_brush_buttons(self):
        self.dot_style.custom_pack(location=tk.RIGHT)
        self.line_style.custom_pack(location=tk.RIGHT)
        self.polygon_style.custom_pack(location=tk.RIGHT)
