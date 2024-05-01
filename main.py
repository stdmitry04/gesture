import cv2
from ultralytics import YOLO
import time
import platform
import pyautogui
import subprocess
import os
model = YOLO('best-2.onnx')

#names: {0: 'collapsed', 1: 'full', 2: 'stop', 3: 'volumedown', 4: 'volumeup'}

last_action = None
def perform_action(classes):
    global last_action
    if classes == [4.0]:
        # Increase volume using AppleScript
        if platform.system() == 'Darwin':  # macOS
            subprocess.run(['osascript', '-e', 'set volume output volume (output volume of (get volume settings) + 10)'])
        elif platform.system() == 'Windows':  # Windows
            pyautogui.press('volumeup')
        print("Volume Up")

    elif classes == [3.0]:
        # Decrease volume using AppleScript
        if platform.system() == 'Darwin':  # macOS
            subprocess.run(['osascript', '-e', 'set volume output volume (output volume of (get volume settings) - 10)'])
        elif platform.system() == 'Windows':  # Windows
            pyautogui.press('volumedown')
        print("Volume Down")

    elif classes == [0.0]:
        if last_action != classes:
            if platform.system() == 'Windows':
                pyautogui.hotkey('winleft', 'down')
            elif platform.system() == 'Darwin':  # macOS
                pyautogui.hotkey('esc')
            print("Minimize Window")

            last_action = classes
        else: pass

    elif classes == [1.0]:
        if last_action != classes:
            if platform.system() == 'Windows':
                pyautogui.hotkey('winleft', 'up')
            elif platform.system() == 'Darwin':  # macOS
                pyautogui.hotkey('f')
            print("Maximize Window")

            last_action = classes
        else: pass

    elif classes == [2.0]:
        if last_action != classes:
            pyautogui.press('space')
            print("Pause/Resume Video")
            last_action = classes
        else: pass
    else:
        #last_action = classes
        print("Unknown Action")

def predict_objects(image):
    results = model.predict(image, save=False, conf=0.70, nms=True)  # Predict objects in the image
    try:
        class_ids = [r.boxes.cls.item() for r in results]
        print(class_ids)
        print(type(class_ids))
        return class_ids
    except:
        print('error')
        last_action = None
        return None


# Main function to capture frames and predict objects
def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
    # Open camera

    while True:
        start_time = time.time()

        ret, frame = cap.read()

        classes = predict_objects(frame)
        if classes:
            perform_action(classes)
        else:
            pass

        time_to_wait = 0.35 - (time.time() - start_time)
        if time_to_wait > 0:
            time.sleep(time_to_wait)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()



