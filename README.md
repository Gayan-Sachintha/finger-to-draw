# Virtual Drawing Board

This project implements a virtual drawing board using OpenCV and MediaPipe for hand gesture recognition. The application allows users to draw on a virtual canvas by using their hand movements, with the ability to change drawing colors through virtual buttons.

## Features
- Draw on a virtual canvas by moving your index finger.
- Change the drawing color by hovering over colored buttons.
- Clear the canvas with a key press.
- Quit the application with a key press.

## Requirements
To run the project, you need the following:
- Python 3.7+
- OpenCV
- MediaPipe
- NumPy

## Installation
1. Clone this repository or download the script.
2. Install the required Python packages:
   ```bash
   pip install opencv-python mediapipe numpy
   ```

## Usage
1. Run the script:
   ```bash
   python virtual_drawing_board.py
   ```
2. Use your hand to interact with the drawing board:
   - Extend your index finger to draw on the canvas.
   - Hover over the colored buttons at the top of the screen to change the drawing color.
   - Press `c` to clear the canvas.
   - Press `q` to quit the application.

## How It Works
- **Hand Tracking**: The script uses MediaPipe's Hand solution to detect and track hand landmarks in real-time.
- **Finger Detection**: By analyzing the relative positions of hand landmarks, the script determines if the index finger is extended.
- **Drawing**: If the index finger is extended, the script draws a line on the virtual canvas following the finger's movement.
- **Color Selection**: Hovering over virtual color buttons changes the drawing color.

## Virtual Buttons
- **Red**: Position `(50, 50)`, Color `(0, 0, 255)`
- **Green**: Position `(150, 50)`, Color `(0, 255, 0)`
- **Blue**: Position `(250, 50)`, Color `(255, 0, 0)`

## Keyboard Controls
- `c`: Clear the canvas.
- `q`: Quit the application.

## Code Highlights
- **Hand Detection**:
  ```python
  hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
  result = hands.process(rgb_frame)
  ```
- **Drawing**:
  ```python
  if extended_fingers == 1:
      cv2.line(canvas, (prev_x, prev_y), (x, y), draw_color, thickness)
  ```
- **Color Change**:
  ```python
  for name, button in buttons.items():
      if is_point_in_button(x, y, button["position"]):
          draw_color = button["color"]
  ```

## Future Enhancements
- Add more color options.
- Implement an eraser tool.
- Save the canvas as an image.
- Enhance gesture recognition for additional tools and actions.

## License
This project is licensed under the MIT License.
