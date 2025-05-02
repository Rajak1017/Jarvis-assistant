import cv2
import traceback
from ultralytics import YOLO
import pyttsx3
import math

def send_output(message):
    print(message)

def draw_extended_corners_rectangle(img, top_left, bottom_right, color, thickness):
    x1, y1 = top_left
    x2, y2 = bottom_right
    corner_length = int((x2 - x1) * 0.05)

    cv2.line(img, (x1, y1), (x2, y1), color, thickness)
    cv2.line(img, (x2, y1), (x2, y2), color, thickness)
    cv2.line(img, (x2, y2), (x1, y2), color, thickness)
    cv2.line(img, (x1, y2), (x1, y1), color, thickness)

    cv2.line(img, (x1, y1), (x1 + corner_length, y1), color, thickness)
    cv2.line(img, (x1, y1), (x1, y1 + corner_length), color, thickness)
    cv2.line(img, (x2, y1), (x2 - corner_length, y1), color, thickness)
    cv2.line(img, (x2, y1), (x2, y1 + corner_length), color, thickness)
    cv2.line(img, (x2, y2), (x2 - corner_length, y2), color, thickness)
    cv2.line(img, (x2, y2), (x2, y2 - corner_length), color, thickness)
    cv2.line(img, (x1, y2), (x1 + corner_length, y2), color, thickness)
    cv2.line(img, (x1, y2), (x1, y2 - corner_length), color, thickness)

def object_detection():
    try:
        model = YOLO('__pycache__\\yolov8l.pt')
        with open('objname\\object.name', 'r') as class_file:
            labels = class_file.read().strip().split('\n')

        cap = cv2.VideoCapture(0)

        while True:
            success, img = cap.read()
            if not success:
                send_output("Error: Unable to access webcam.")
                break

            results = model(img, stream=True)
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    thickness = 4
                    color = (0, 0, 200)

                    draw_extended_corners_rectangle(img, (x1, y1), (x2, y2), color, thickness)

                    conf = round(box.conf[0].item(), 2)
                    cls = int(box.cls[0])
                    text = f'{labels[cls]} {conf}'

                    cv2.putText(img, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            cv2.imshow("Object Detection", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    except Exception as e:
        send_output(f"Error during object detection: {traceback.format_exc()}")
def stop_obj_detection():
    """
    Sets the global flag to stop detection.
    """
    global stop_detection
    stop_detection = True