import tkinter as tk
from GUI.bar_button import BarButton


class SideBar(tk.Frame):
    """
    Frame for __sidebar widgets. It creates all buttons on left side.
    """

    def __init__(self, master: tk.Tk, bg_color: str, width: int) -> None:
        """
        Initializes __sidebar frame
        :param master: root that contains the __sidebar
        :param bg_color: background outline_color of the __sidebar
        :param width: width of __sidebar frame
        """
        # Initializing tkinter.Frame with given parameters
        super().__init__(master, bg=bg_color, width=width)
        # Setting up button on frame
        self._setup_sidebar_buttons()

    def _setup_sidebar_buttons(self) -> None:
        """
        Function that sets up buttons for __sidebar frame.
        Buttons are placed in __sidebar frame:
        :return: None
        """
        # TOP BUTTONS
        # Brush – button that activates brush tool
        self.brush_button = BarButton(self, 'brush.png', 'brush')
        self.brush_button.custom_pack(location=tk.TOP)

        # Eraser - button that activates eraser tool
        self.eraser_button = BarButton(self, 'eraser.png', 'eraser')
        self.eraser_button.custom_pack(location=tk.TOP)

        # Figures - button that activates __figure drawing
        self.figures_button = BarButton(self, 'figures.png', 'figures')
        self.figures_button.custom_pack(location=tk.TOP)

        # Text - button that activates text writing on canvas
        self.text_button = BarButton(self, 'text.png', 'text')
        self.text_button.custom_pack(location=tk.TOP)

        # Select - button that activates select tool
        self.select_button = BarButton(self, 'select.png', 'select')
        self.select_button.custom_pack(location=tk.TOP)

        # Trash - button that clears all canvas
        self.clear_button = BarButton(self, 'clear.png', 'clear all')
        self.clear_button.custom_pack(location=tk.TOP)

        # Background – button that opens outline_color palette for changing background outline_color
        self.background_button = BarButton(self, 'background.png', 'background outline_color')
        self.background_button.custom_pack(location=tk.TOP)

        # Undo - button that undoes last change on canvas
        self.undo_button = BarButton(self, 'undo.png', 'undo')
        # Stating button to be disabled because there is nothing to undo yet
        self.undo_button['state'] = 'disabled'
        self.undo_button.custom_pack(location=tk.TOP)

        # Redo - button that redoes last undone change on canvas
        self.redo_button = BarButton(self, 'redo.png', 'redo')
        # Stating button to be disabled because there is nothing to redo yet
        self.redo_button['state'] = 'disabled'
        self.redo_button.custom_pack(location=tk.TOP)

        # BOTTOM BUTTONS
        # Save – button that saves canvas as image
        self.save_button = BarButton(self, 'save.png', 'save')
        self.save_button.custom_pack(location=tk.BOTTOM)

        # Color - button that opens outline_color palette for changing outline_color of brush or painted object
        # self.color_button = BarButton(self, text='brush outline_color')
        # self.color_button.custom_pack(location=tk.BOTTOM)

    def custom_pack(self) -> None:
        """
        Custom pack of sidebar widget on window
        :return: None
        """
        self.pack(side=tk.LEFT, fill=tk.BOTH)
