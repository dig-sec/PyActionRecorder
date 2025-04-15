# PyActionRecorder
Automate tasks by recording and replaying mouse and keyboard actions. Streamline your workflow with customizable replay speeds and intelligent input detection.

## Features

- Record mouse clicks, holds, and keyboard inputs with precise timing
- Replay recorded macros with adjustable speed
- Save recordings with automatic timestamps
- Load previously saved macros
- Interrupt replay at any time with stop key (F4)
- Simple menu-driven interface

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

- Failsafe mechanism included via PyAutoGUI
If you quickly move your mouse to any corner of the screen (typically the upper-left corner), PyAutoGUI will raise an exception and stop the script.

## Requirements

- Python 3.x
- `pynput` library (`pip install pynput`)
- `pyautogui` library (`pip install pyautogui`)
