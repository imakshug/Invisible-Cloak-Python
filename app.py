from flask import Flask, render_template, Response, jsonify, request
import cv2
import numpy as np
import threading
import time

app = Flask(__name__)


class InvisibleCloak:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.background = None
        self.is_running = False
        self.cloak_color = 'red'
        self.color_ranges = {
            'red': {
                'lower1': np.array([0, 120, 70]),
                'upper1': np.array([10, 255, 255]),
                'lower2': np.array([170, 120, 70]),
                'upper2': np.array([180, 255, 255])
            },
            'blue': {
                'lower1': np.array([100, 150, 0]),
                'upper1': np.array([140, 255, 255]),
                'lower2': np.array([100, 150, 0]),
                'upper2': np.array([140, 255, 255])
            },
            'green': {
                'lower1': np.array([40, 150, 0]),
                'upper1': np.array([80, 255, 255]),
                'lower2': np.array([40, 150, 0]),
                'upper2': np.array([80, 255, 255])
            }
        }
        self.capture_background()

    def capture_background(self):
        print("Capturing background...")
        time.sleep(2)
        for i in range(30):
            ret, back = self.cap.read()
            if ret:
                self.background = np.flip(back, axis=1)

    def get_frame(self):
        if not self.cap.isOpened():
            return None

        ret, img = self.cap.read()
        if not ret:
            return None

        img = np.flip(img, axis=1)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Get color range based on selected color
        color_range = self.color_ranges[self.cloak_color]

        # Create masks
        mask1 = cv2.inRange(hsv, color_range['lower1'], color_range['upper1'])
        mask2 = cv2.inRange(hsv, color_range['lower2'], color_range['upper2'])
        mask = mask1 + mask2

        # Remove noise
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,
                                np.ones((5, 5), np.uint8))

        # Replace cloak area with background
        if self.background is not None:
            img[np.where(mask == 255)] = self.background[np.where(mask == 255)]

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', img)
        if ret:
            return buffer.tobytes()
        return None

    def set_color(self, color):
        if color in self.color_ranges:
            self.cloak_color = color
            return True
        return False

    def stop(self):
        self.is_running = False


# Global cloak instance
cloak = InvisibleCloak()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            frame = cloak.get_frame()
            if frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.033)  # ~30 FPS

    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/set_color', methods=['POST'])
def set_color():
    data = request.json
    color = data.get('color', 'red')
    success = cloak.set_color(color)
    return jsonify({'success': success, 'color': color})


@app.route('/stop', methods=['POST'])
def stop_video():
    cloak.stop()
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
