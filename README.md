# PDF Combiner

A simple desktop application to combine multiple PDF files into a single PDF with drag-and-drop reordering and theme switching capabilities.

## Features

- Modern user interface with dark/light theme support
- Drag and drop file reordering
- Manual file reordering with up/down buttons
- Combine multiple PDFs into a single file
- Simple and intuitive interface
- Cross-platform support

## Requirements

- Python 3.7 or higher (tested with Python 3.13.4)
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone or download this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python pdf_combiner.py
   ```
2. Click "Add PDF" to select PDF files
3. Reorder files by:
   - Dragging and dropping files in the list
   - Using "Move Up" and "Move Down" buttons
4. Click "Combine PDFs" to merge the selected files
5. Choose where to save the combined PDF
6. Use "Clear List" to remove all selected files
7. Toggle between dark and light themes using the theme button (🌙/☀️)

## Building Executable

To create a standalone executable:

1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```
2. Create the executable:
   ```
   pyinstaller --onefile --windowed pdf_combiner.py
   ```
3. The executable will be created in the `dist` folder

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License. 