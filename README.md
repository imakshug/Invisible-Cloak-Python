# Invisible Cloak 

This project uses OpenCV and NumPy to create an "invisible cloak" effect in real-time video. When a red cloth is shown to the camera, it is replaced by the background, making it appear invisible.

## Usage

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the script:
   ```
   python main.py
   ```
3. Press `q` to exit.

## Requirements

- Python 3.x
- OpenCV
- NumPy

## How it Works

- Captures the background.
- Detects red color in each frame.
- Replaces red areas with the background.