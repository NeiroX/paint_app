# Paint App
### Paint App is a simple drawing application built with Tkinter in Python.


## Installation

1. Download paint_app.zip and unpack it.
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
## Usage

Run the following command to start the application:

```bash
python main.py
```

## Features
### Drawing tools

1. **Brush**
  1. Ability to change brush color. Default brush color is `#00000`.
  2. Ability to change brush width
  3. Brush paints centered dots according to brush color and brush width. In code it's represented by ```class Paint```
  4. Group of painted dots is a group which contains all painted dots from moment of click on Left Mouse Button until Left Mouse Button release. In code it's represented by ```class PaintGroup```
  5. Brush is represented in code by ```class Brush``` which inherits ```class BasicTool```
2. **Eraser**
  1. Ability to change eraser width
  2. Eraser uses object erasing
  3. Eraser is represented in code by ```class Eraser``` which inherits ```class BasicTool```
4. **Figures**
  1. ```class Outline``` represents the settings of figure outline.
  2. ```class FillFigure``` represents the settings of figure filling.
  3. Ability to draw line. Line is represented in code by ```class Line``` which inherits from ```class Outline```.
  4. Ability to draw Rectangle, Triangle, Oval, Polygon. Figures are presented in code by ```class Figure``` which inherits from ```class Outline``` and ```class FillFigure```.
  5. Ability to change settings such as width and color of figure outline and in addition to ```class Figure``` ability to change fill color.
  6. In code figure creating tool is represented by ```class FigureDrawing```.
5. **Text**
  1. Ability to change font family.
  2. Ability to change font size.
  3. Ability to change font color.
  4. In code text writing tool is represented by ```class Texting```.
7. **Select**
  1. Select tool let user select object on canvas and then change its settings such as position, layer, color, width and others.
  2. Topbar adapts to selected object type.

### Undo/Redo functions

App uses ```deque``` or in other words stack to store changes on canvas. Changes are repsented by 4 types: by class of object, by ```BackgroundChange``` which tracks canvas background changing, by ```class DeleteObjectChange``` which represents performed action to delete object from canvas, by ```SelectedChange``` which tracks changes when the object is selected. 
```SelectedChange``` stores previous and new copies of object and according to action returns one of them to canvas.

### Canvas feautures

1. Canvas has ability to change its color. Default canvas color is `#ffffff`.
2. Ability to save canvas as image in format .jpeg.
3. Opportunity to save canvas to .json file and continue to edit the same canvas project later. Canvas project saves by itself when application window is closed by special button with door icon.

### GUI

User friendly and adaptive GUI is represented by 2 bars: sidebar (```class SideBar```) and topbar (```class TopBar```). Both of them inherit from ```tkinter.Frame``` and contain custom ```tkinter.Button``` buttons that their settings are stored in ```class BarButton```.
Sidebar contains tools buttons and buttons: Undo, Redo, Save as image, Save and close, Clear all, Background color.
Topbar adapts to chosen tool and situation.
All GUI classes are wired up in ```class ApplicationGUI``` which inherits from ```tkinter.Tk```.

### App logic

Constants are placed in file _setting.py_
Main logic is separated between models and in mostly found in ```class CanvasManager```.

