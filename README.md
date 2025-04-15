# PyActionRecorder
Automate tasks by recording and replaying mouse and keyboard actions. Streamline your workflow with customizable replay speeds and intelligent input detection.

## Features

- Record mouse clicks, holds, and keyboard inputs with precise timing
- Replay recorded macros with adjustable speed
- Save recordings with automatic timestamps
- Load previously saved macros
- Intelligent detection of mouse clicks vs. holds
- Interrupt replay at any time with stop key (F4)
- Simple menu-driven interface

## Requirements

- Python 3.x
- `pynput` library (`pip install pynput`)
- `pyautogui` library (`pip install pyautogui`)
- Or install all dependencies: `pip install -r requirements.txt`

## How to Use

1. **Record New Macro**: Capture your mouse and keyboard actions (press ESC to stop recording)
2. **Load Macro**: Select a previously saved recording
3. **List Macros**: View all available saved recordings
4. **Replay Macro**: Run your macro with customizable loop count and speed factor
5. **Exit**: Close the application

## Getting Started

```bash
# Clone the repository
git clone https://github.com/dig-sec/PyActionRecorder.git
cd PyActionRecorder

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Technical Details

- Recordings are saved as JSON files with timestamps
- Mouse hold detection based on configurable duration threshold
- Supports all mouse buttons (left, right, middle)
- Full keyboard support including special keys
- Failsafe mechanism included via PyAutoGUI