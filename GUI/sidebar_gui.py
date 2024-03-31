import tkinter as tk
from GUI.bar_button import BarButton


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
        self.trash_button = BarButton(self, 'clear.png', 'clear all')
        self.trash_button.custom_pack(location=tk.TOP)

        # Background – button that opens color palette for changing background color
        self.background_button = BarButton(self, 'background.png', 'background color')
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

        # Color - button that opens color palette for changing color of brush or painted object
        # self.color_button = BarButton(self, text='brush color')
        # self.color_button.custom_pack(location=tk.BOTTOM)
