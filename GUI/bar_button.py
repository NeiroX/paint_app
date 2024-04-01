import tkinter as tk
import os
from settings import BUTTONS_PADDING, REGULAR_COLOR, ICONS_DIR, BUTTON_HOVER_COLOR
from typing import Callable, Any, Literal
from PIL import Image, ImageTk


class BarButton(tk.Button):
    """
    Custom button for the __sidebar.
    This class inherits from tkinter.Button and contains button setup, custom settings and custom pack.
    """

    def __init__(self, master: Any, image_name: str = '', text: str = '', display_text=False,
                 compound: Literal['left', 'right'] = tk.LEFT) -> None:
        """
        Constructor for the __sidebar button.
        :param master: master Widget that will contain the button
        :param image_name: image name for the button icon
        :param text: text for the button to be displayed
        :param display_text: whether display text
        :return: None
        """
        # Setting custom settings for tkinter.Button
        super().__init__(master=master, relief=tk.RAISED, padx=BUTTONS_PADDING, pady=BUTTONS_PADDING, borderwidth=0,
                         compound=compound, highlightthickness=0, bg='white')
        # Variables that can be updated
        self._image = BarButton.get_image(image_name) if image_name else None
        self._text = text.capitalize()
        self._command = None
        self._display_text = display_text
        self._state = True

        # Setup button displaying
        self._setup_button()

    def _setup_button(self) -> None:
        """
        Function that sets up the button settings like icon and text.
        :return: None
        """
        if self._display_text:
            self['text'] = self._text
        # Setting action when button is pressed
        self['command'] = self._command
        # If there is an image name then we set icon within button.
        # Otherwise, it's outline_color button and its background might be changed
        if self._image:
            self['image'] = self._image
        else:
            self['bg'] = 'white'
            self['fg'] = 'black'

        def _on_enter(event: Any) -> None:
            """
            Function that change button appearance when it's pressed
            :param event: event information
            :return: None
            """
            self['background'] = BUTTON_HOVER_COLOR

        def _on_leave(event: Any) -> None:
            """
            Function that change button appearance to default after it was pressed
            :param event: event information
            :return:
            """
            self['background'] = REGULAR_COLOR

        self.bind("<Enter>", _on_enter)
        self.bind("<Leave>", _on_leave)

    def change_button_color(self, color: str) -> None:
        """
        Function to change button color to given color
        :param color: a color from type str
        :return: None
        """
        self.configure(background=color, foreground=color)

    def set_command(self, new_command: Callable) -> None:
        """
        Function that sets up action when button is pressed
        :param new_command:
        :return: None
        """
        self._command = new_command
        self._setup_button()

    def is_enabled(self, status: bool) -> None:
        """
        Function to change button state between disabled and normal states
        :param status: boolean variable represents whether button is enabled or not
        :return: None
        """
        if status:
            self.configure(state='normal')
            self._state = True
        else:
            self.configure(state='disabled')
            self._state = False

    def get_state(self) -> bool:
        """
        Function that returns whether button is enabled or not
        :return state: boolean variable represents whether button is enabled or not
        """
        return self._state

    def custom_pack(self, location: Literal['left', 'right'] = tk.TOP) -> None:
        """
        Function that packs button on master frame according to the given location.
        :param location: string variable that stores the location of the button on the master frame
        :return: None
        """
        self.pack(pady=BUTTONS_PADDING, padx=BUTTONS_PADDING, side=location)

    @staticmethod
    def get_image(image_name: str) -> tk.PhotoImage:
        """
        Function that returns the image according to the given image name.
        :param image_name:
        :return: PhotoImage object of the given image name
        """
        # If unable to find image then throw an error and message about the error.
        full_path_to_image = os.path.join(ICONS_DIR, image_name)
        try:
            image = ImageTk.PhotoImage(Image.open(full_path_to_image).resize((20, 20)))
        except Exception:
            print('Could not load image: ', full_path_to_image)
            image = None
        return image
