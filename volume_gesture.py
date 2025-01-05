import cv2
import mediapipe as mp
import pyautogui

x1 = y1 = x2 = y2 = 0

cap = cv2.VideoCapture(0)
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

while True:
    ret, img = cap.read()
    if not ret:
        break

    img = cv2.flip(img, 1)
    frame_height, frame_width, _ = img.shape
    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(img, hand, mp.solutions.hands.HAND_CONNECTIONS)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:  
                    cv2.circle(img=img, center=(x, y), radius=8, color=(0, 255, 255), thickness=3)
                    x1 = x
                    y1 = y
                if id == 4:  
                    cv2.circle(img=img, center=(x, y), radius=8, color=(0, 0, 255), thickness=3)
                    x2 = x
                    y2 = y
        dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 // 4
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 5)
        if dist > 50:
            pyautogui.press("volumeup")
        else:
            pyautogui.press("volumedown")

    cv2.imshow("volume control", img)
    key = cv2.waitKey(1)  
    if key == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()
