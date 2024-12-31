import cv2
import mediapipe as mp
import numpy as np
import time


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)


cap = cv2.VideoCapture(0)


canvas = None


draw_color = (0, 255, 0)  
thickness = 5  


prev_x, prev_y = None, None


last_tap_time = 0
tap_timeout = 1.0  


buttons = {
    "red": {"position": (50, 50), "color": (0, 0, 255)},
    "green": {"position": (150, 50), "color": (0, 255, 0)},
    "blue": {"position": (250, 50), "color": (255, 0, 0)},
}


def is_point_in_button(x, y, button_position, button_size=40):
    bx, by = button_position
    return bx - button_size <= x <= bx + button_size and by - button_size <= y <= by + button_size


def count_extended_fingers(hand_landmarks):
    
    finger_tips = [8, 12, 16, 20]  
    finger_bases = [6, 10, 14, 18]  
    
    extended_fingers = 0
    for tip, base in zip(finger_tips, finger_bases):
        if hand_landmarks[tip].y < hand_landmarks[base].y:  
            extended_fingers += 1

    
    thumb_tip = hand_landmarks[4]
    thumb_base = hand_landmarks[3]
    if abs(thumb_tip.x - thumb_base.x) > 0.1:  
        extended_fingers += 1

    return extended_fingers

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    
    if canvas is None:
        canvas = np.zeros_like(frame)

    
    result = hands.process(rgb_frame)

    
    for name, button in buttons.items():
        cv2.circle(frame, button["position"], 40, button["color"], -1)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            
            index_finger_tip = hand_landmarks.landmark[8]
            x = int(index_finger_tip.x * frame.shape[1])
            y = int(index_finger_tip.y * frame.shape[0])

            
            for name, button in buttons.items():
                if is_point_in_button(x, y, button["position"]):
                    
                    if time.time() - last_tap_time > tap_timeout:
                        last_tap_time = time.time()  
                        draw_color = button["color"]  
                        break

            
            extended_fingers = count_extended_fingers(hand_landmarks.landmark)

            
            if extended_fingers == 1:
                if prev_x is not None and prev_y is not None:
                    cv2.line(canvas, (prev_x, prev_y), (x, y), draw_color, thickness)
                prev_x, prev_y = x, y
            else:
                prev_x, prev_y = None, None

    else:
        
        prev_x, prev_y = None, None

    
    combined_frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

    
    cv2.putText(combined_frame, "", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(combined_frame, "", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(combined_frame, "", (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    
    cv2.imshow("Virtual Drawing Board", combined_frame)

    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):  
        canvas = np.zeros_like(frame)
    elif key == ord('q'):  
        break

cap.release()
cv2.destroyAllWindows()
