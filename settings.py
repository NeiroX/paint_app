import os

# Sizes
DEFAULT_SCREEN_WIDTH = 1080
DEFAULT_SCREEN_HEIGHT = 720
CANVAS_WIDTH = 900
CANVAS_HEIGHT = 600
SIDEBAR_WIDTH = 150
TOPBAR_HEIGHT = 80

# Padding
DEFAULT_CANVAS_PADDING = 100
BUTTONS_PADDING = 10

# Colors
PRIMARY_COLOR = '#31363F'
ACCENT_COLOR = '#76ABAE'
DEFAULT_CANVAS_COLOR = 'white'
BUTTON_HOVER_COLOR = 'gray'
BUTTON_ACTIVE_COLOR = 'slateblue'
REGULAR_COLOR = 'lightgray'

# Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(BASE_DIR, 'src/icon')

# Brush style
DEFAULT_BRUSH_SIZE = 5
DEFAULT_BRUSH_COLOR = 'black'

# Figures name
LINE = 'line'
POLYGON = 'polygon'
RECTANGLE = 'rectangle'
TRIANGLE = 'triangle'
OVAL = 'oval'

# Tools name
BRUSH = 'brush'
ERASER = 'eraser'
TEXT = 'text'
SELECT = 'select'
FIGURES = 'figures'

# Text style
FONT_FAMILIES = (
    'Arial', 'Courier', 'Times', 'Helvetica', 'Symbol', 'Courier New', 'Times New Roman', 'Verdana', 'Comic Sans MS')
DEFAULT_TEXT_COLOR = 'black'
DEFAULT_TEXT_FONT = FONT_FAMILIES[0]
DEFAULT_TEXT_SIZE = 12
DEFAULT_FONT = (DEFAULT_TEXT_FONT, DEFAULT_TEXT_SIZE)

# Styles
# SIDE_BUTTON_STYLE = ttk.Style()
# SIDE_BUTTON_STYLE.configure('BarButton.TButton', borderwidth=0, relief='flat', background='#7f7f7f',
#                             foreground='white',
#                             padding=10, font=('Helvetica', 12))
