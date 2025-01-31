import cv2
import numpy as np
import dlib
from math import hypot
import winsound

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
font = cv2.FONT_HERSHEY_PLAIN

keyboard = np.zeros((600, 1000, 3), np.uint8)
keys_set_1 = {0: "Q", 1: "W", 2: "E", 3: "R", 4: "T", 5: "A", 6: "S", 7: "D", 8: "F", 9: "G", 10: "Z", 11: "X", 12: "C", 13: "V", 14: "<"}
keys_set_2 = {0: "Y", 1: "U", 2: "I", 3: "O", 4: "P", 5: "H", 6: "J", 7: "K", 8: "L", 9: "_", 10: "V", 11: "B", 12: "N", 13: "M", 14: "<"}

def letter(letter_index, text, letter_light):
    x, y = (letter_index % 5) * 200, (letter_index // 5) * 200
    width, height, th = 200, 200, 3
    
    if letter_light:
        cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
    else:
        cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (255, 0, 0), th)
    
    font_scale, font_th = 10, 4
    text_size = cv2.getTextSize(text, font, font_scale, font_th)[0]
    text_x = x + (width - text_size[0]) // 2
    text_y = y + (height + text_size[1]) // 2
    cv2.putText(keyboard, text, (text_x, text_y), font, font_scale, (255, 0, 0), font_th)

def draw_menu():
    rows, cols, _ = keyboard.shape
    cv2.line(keyboard, (cols//2, 0), (cols//2, rows), (51, 51, 51), 4)
    cv2.putText(keyboard, "LEFT", (80, 300), font, 6, (255, 255, 255), 5)
    cv2.putText(keyboard, "RIGHT", (cols//2 + 80, 300), font, 6, (255, 255, 255), 5)

def midpoint(p1, p2):
    return (p1.x + p2.x) // 2, (p1.y + p2.y) // 2

def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
    hor_line_length = hypot(left_point[0] - right_point[0], left_point[1] - right_point[1])
    ver_line_length = hypot(center_top[0] - center_bottom[0], center_top[1] - center_bottom[1])
    return hor_line_length / ver_line_length

cap = cv2.VideoCapture(0)
board = np.full((300, 1400), 255, np.uint8)
frames, blinking_frames, letter_index, frames_to_blink, frames_active_letter = 0, 0, 0, 6, 9
keyboard_selected, last_keyboard_selected, text, selected_keyboard_menu = "left", "left", "", True
keyboard_selection_frames = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Debugging: Print the shape and dtype of the gray image
    print(f"Grayscale image dtype: {gray.dtype}, shape: {gray.shape}")

    # Ensure gray is uint8 (8-bit)
    gray = gray.astype(np.uint8)

    # Validate grayscale image is not empty or None
    if gray is None or gray.size == 0:
        print("Error: Invalid grayscale image!")
        continue

    # Print shape of gray to confirm its size
    print(f"Grayscale image shape: {gray.shape}")

    # Validate the image before detection
    faces = []
    try:
        faces = detector(gray)  # This is where the error was occurring
        print(f"Faces detected: {len(faces)}")
    except Exception as e:
        print(f"Error in face detection: {e}")

    if len(faces) == 0:
        print("No faces detected!")

    if selected_keyboard_menu:
        draw_menu()
    else:
        keys_set = keys_set_1 if keyboard_selected == "left" else keys_set_2
        active_letter = keys_set[letter_index]
        for i in range(15):
            letter(i, keys_set[i], i == letter_index)

    for face in faces:
        landmarks = predictor(gray, face)
        if landmarks is None:
            print("Error: No landmarks detected!")
            continue

        gaze_ratio = (get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks) + 
                      get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)) / 2
        if selected_keyboard_menu:
            keyboard_selected = "right" if gaze_ratio <= 0.9 else "left"
            keyboard_selection_frames += 1
            if keyboard_selection_frames == 15:
                selected_keyboard_menu, frames, keyboard_selection_frames = False, 0, 0
                winsound.PlaySound("right.wav" if keyboard_selected == "right" else "left.wav", winsound.SND_ALIAS)
        else:
            if get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks) > 5:
                blinking_frames += 1
                if blinking_frames == frames_to_blink:
                    text += " " if active_letter == "_" else active_letter
                    selected_keyboard_menu, blinking_frames = True, 0

    cv2.putText(board, text, (80, 100), font, 9, 0, 3)
    cv2.imshow("Frame", frame)
    cv2.imshow("Virtual keyboard", keyboard)
    cv2.imshow("Board", board)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
