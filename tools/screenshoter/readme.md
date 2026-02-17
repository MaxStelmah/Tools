# Screenshot Editor

A powerful, full-screen screenshot editing tool built with Python and Tkinter. Capture, annotate, and edit screenshots with an intuitive icon-based toolbar interface.

![filter_img screenshot](https://github.com/MaxStelmah/Tools/blob/eff5dbd7440820ac6f77ae1b343d5299d2615183/tools/screenshoter/assets/Screenshoter_UI.png?raw=true "Screenshot")

## Features

- **Full-screen editing interface** - Maximizes workspace for screenshot editing
- **Icon-based toolbar** - Easy-to-use visual interface with tooltips
- **Multiple drawing tools**:
  - Arrow drawing
  - Rectangle outlining
  - Solid bar/rectangle filling
  - Text annotation
  - Area blurring (for privacy)
  - Image cropping
- **Color customization** - Choose any color for your annotations
- **Undo functionality** - Revert mistakes with Ctrl+Z
- **Auto-scaling** - Screenshots automatically scale to fit the screen while maintaining quality
- **Keyboard shortcuts** - Quick access to common functions

## Requirements

- Python 3.x
- Required Python packages:
```
  pyautogui
  Pillow (PIL)
  opencv-python (cv2)
  numpy
  tkinter (usually included with Python)
```

## Installation

1. Clone or download this repository

2. Install required dependencies:
```bash
   pip install pyautogui Pillow opencv-python numpy
```

3. Create a `gui` folder in the same directory as the script

4. Add icon files (24x24 PNG images) to the `gui` folder with the following names:
   - `arrow.png` - Arrow drawing tool
   - `rectangle.png` - Rectangle drawing tool
   - `blur.png` - Blur tool
   - `color.png` - Color picker
   - `bar.png` - Solid bar/rectangle tool
   - `text.png` - Text annotation tool
   - `cut.png` - Crop tool
   - `save.png` - Save button
   - `undo.png` - Undo button
   - `exit.png` - Exit button

## Usage

### Basic Usage

Run the script from the command line:
```bash
python screen.py <save_folder> [--title <window_title>]
```

**Parameters:**
- `save_folder` (required) - Path to the folder where screenshots will be saved
- `--title` (optional) - Custom window title (default: "tk")

**Example:**
```bash
python screen.py ./screenshots --title "My Screenshot Editor"
```

### Keyboard Shortcuts

- **Ctrl+Z** - Undo the last action
- **Enter** - Save and exit
- **Escape** - Toggle fullscreen mode

### Toolbar Tools

1. **Arrow Tool** - Draw arrows to point out specific areas
2. **Rectangle Tool** - Draw outlined rectangles
3. **Blur Tool** - Blur sensitive information
4. **Color Picker** - Change the color of drawing tools
5. **Bar Tool** - Draw filled rectangles
6. **Text Tool** - Add text annotations
7. **Cut Tool** - Crop the image to a selected area
8. **Save** - Save the current screenshot
9. **Undo** - Revert the last change
10. **Exit** - Close the application

### How to Use Tools

1. **Launch the application** - The tool automatically captures a screenshot when started
2. **Select a tool** from the toolbar by clicking its icon
3. **Click and drag** on the canvas to apply the tool:
   - For arrows and rectangles: Click at the start point, drag to the end point
   - For text: Click where you want to place text, then enter text in the dialog
   - For blur: Select the area you want to blur
   - For cut: Select the area you want to keep (everything else will be removed)
4. **Change colors** by clicking the color picker icon
5. **Save your work** by clicking the save icon or pressing Enter
6. **Undo mistakes** with Ctrl+Z or the undo button

## File Naming Convention

Screenshots are automatically saved with timestamps:
```
screenshot_YYYYMMDD_HHMMSS.png
```

Example: `screenshot_20260207_143025.png`

## Features in Detail

### Auto-Scaling
The application automatically scales large screenshots to fit your screen while preserving the original resolution for editing and saving. All edits are performed on the full-resolution image.

### Full-Screen Mode
The application opens in full-screen mode by default, providing maximum workspace. Press Escape to toggle full-screen mode on/off.

### Tooltips
Hover over any toolbar button to see a tooltip describing its function.

### Visual Feedback
The currently selected tool is highlighted with a sunken button appearance, making it easy to see which tool is active.

## Troubleshooting

### Icons Not Displaying
- Ensure the `gui` folder exists in the same directory as `screen.py`
- Verify all icon PNG files are present and correctly named
- Check file permissions to ensure the script can read the icons
- If icons are missing, the toolbar will display text labels as fallback

### Screenshot Quality
- The tool preserves the original screenshot resolution regardless of display scaling
- Edits are performed on the full-resolution image
- Saved screenshots maintain original quality

### Font Issues
- If text annotation fails, ensure Arial font is available on your system
- On Linux, you may need to install Microsoft fonts:
```bash
  sudo apt-get install ttf-mscorefonts-installer
```

## Customization

### Changing Icon Size
Modify the `icon_size` variable in the `create_toolbar` method:
```python
icon_size = (32, 32)  # Change from (24, 24) to larger icons
```

### Changing Default Color
Modify the `current_color` initialization in `__init__`:
```python
self.current_color = (0, 255, 0)  # Green instead of red
```

### Adjusting Arrow Size
Modify the arrow parameters in the `draw_arrow` function:
```python
arrow_length = 30  # Longer arrowhead
arrow_width = 15   # Wider arrowhead
```

## License

This project is open source and available for personal and commercial use.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit pull requests.

## Acknowledgments

Built with:
- [PyAutoGUI](https://pyautogui.readthedocs.io/) - Screenshot capture
- [Pillow](https://python-pillow.org/) - Image processing
- [OpenCV](https://opencv.org/) - Image filtering and effects
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - GUI framework