import tkinter as tk
from typing import Any, Callable
from settings import BUTTONS_PADDING, ICONS_DIR, BUTTON_HOVER_COLOR, BUTTON_ACTIVE_COLOR, REGULAR_COLOR
from PIL import Image, ImageTk
import os


class SideBar(tk.Frame):
    """
    Frame for sidebar widgets. It creates all buttons.
    """

    def __init__(self, root: tk.Tk, bg_color: str, width: int) -> None:
        """
        Initializes sidebar frame
        :param root: root that contains the sidebar
        :param bg_color: background color of the sidebar
        :param width: width of sidebar frame
        """
        # Initializing tkinter.Frame with given parameters
        super().__init__(root, bg=bg_color, width=width)
        # Setting up button on frame
        self._setup_sidebar_buttons()

    def _setup_sidebar_buttons(self) -> None:
        """
        Function that sets up buttons for sidebar frame.
        Buttons are placed in sidebar frame:
        :return: None
        """
        # TOP BUTTONS
        # Brush – button that activates brush tool
        self.brush_button = SideBarButton(self, 'brush.png', 'brush')
        self.brush_button.custom_pack()

        # Eraser - button that activates eraser tool
        self.eraser_button = SideBarButton(self, 'eraser.png', 'eraser')
        self.eraser_button.custom_pack()

        # Figures - button that activates figure drawing
        self.figures_button = SideBarButton(self, 'figures.png', 'figures')
        self.figures_button.custom_pack()

        # Text - button that activates text writing on canvas
        self.text_button = SideBarButton(self, 'text.png', 'text')
        self.text_button.custom_pack()

        # Select - button that activates select tool
        self.select_button = SideBarButton(self, 'select.png', 'select')
        self.select_button.custom_pack()

        # Trash - button that clears all canvas
        self.trash_button = SideBarButton(self, 'clear.png', 'clear all')
        self.trash_button.custom_pack()

        # Undo - button that undoes last change on canvas
        self.undo_button = SideBarButton(self, 'undo.png', 'undo')
        # Stating button to be disabled because there is nothing to undo yet
        self.undo_button['state'] = 'disabled'
        self.undo_button.custom_pack()

        # Redo - button that redoes last undone change on canvas
        self.redo_button = SideBarButton(self, 'redo.png', 'redo')
        # Stating button to be disabled because there is nothing to redo yet
        self.redo_button['state'] = 'disabled'
        self.redo_button.custom_pack()

        # Save – button that saves canvas as image
        self.save_button = SideBarButton(self, 'save.png', 'save')
        self.save_button.custom_pack()

        # BOTTOM BUTTONS
        # Background – button that opens color palette for changing background color
        self.background_button = SideBarButton(self, 'background.png', 'background color')
        self.background_button.custom_pack(tk.BOTTOM)

        # Color - button that opens color palette for changing color of brush or painted object
        self.color_button = SideBarButton(self, text='brush color')
        self.color_button.custom_pack(tk.BOTTOM)


class SideBarButton(tk.Button):
    """
    Custom button for the sidebar.
    This class inherits from tkinter.Button and contains button setup, custom settings and custom pack.
    """

    def __init__(self, master: Any, image_name: str = '', text: str = '') -> None:
        """
        Constructor for the sidebar button.
        :param master: master Widget that will contain the button
        :param image_name: image name for the button icon
        :param text: text for the button to be displayed
        :return: None
        """
        # Setting custom settings for tkinter.Button
        super().__init__(master=master, relief=tk.RAISED, padx=BUTTONS_PADDING, pady=BUTTONS_PADDING, borderwidth=0,
                         compound=tk.LEFT, highlightthickness=0, bg='white')
        # Variables that can be updated
        self._image = SideBarButton.get_image(image_name) if image_name else None
        self._text = text.capitalize()
        self._command = None

        # Setup button displaying
        self._setup_button()

    def _setup_button(self) -> None:
        """
        Function that sets up the button settings like icon and text.
        :return: None
        """
        # self['text'] = self._text
        # Setting action when button is pressed
        self['command'] = self._command
        # If there is an image name then we set icon within button.
        # Otherwise, it's color button and its background might be changed
        if self._image:
            self['image'] = self._image
        else:
            self['bg'] = 'white'
            self['fg'] = 'white'

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

    def set_command(self, new_command: Callable) -> None:
        """
        Function that sets up action when button is pressed
        :param new_command:
        :return: None
        """
        self._command = new_command
        self._setup_button()

    def disable(self) -> None:
        self.configure(state='disabled')

    def enable(self) -> None:
        self.configure(state='normal')

    def custom_pack(self, location: str = tk.TOP) -> None:
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
        :return:
        """
        # If unable to find image then throw an error and message about the error.
        full_path_to_image = os.path.join(ICONS_DIR, image_name)
        try:
            image = ImageTk.PhotoImage(Image.open(full_path_to_image).resize((20, 20)))
        except BaseException:
            print('Could not load image: ', full_path_to_image)
            image = None
        return image
