import threading
import pickle
import cv2
import mediapipe as mp
import numpy as np
from keras.preprocessing.sequence import pad_sequences

# Global flag to manage thread state
stop_detection = False

def detect_signs():
    """
    Function to detect hand signs using Mediapipe and a pre-trained model.
    Runs in a separate thread to avoid blocking the main program.
    """
    global stop_detection

    # Load the model and labels
    model_path = '__pycache__\\model.p'
    try:
        model_dict = pickle.load(open(model_path, 'rb'))
        model = model_dict['model']
    except FileNotFoundError:
        print(f"Model file not found at {model_path}. Please check the path.")
        return
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Label mapping
    labels_dict = {
        0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8', 8: '9',
        9: 'A', 10: 'B', 11: 'C', 12: 'D', 13: 'E', 14: 'F', 15: 'G', 16: 'H',
        17: 'I', 18: 'J', 19: 'K', 20: 'L', 21: 'M', 22: 'N', 23: 'O', 24: 'P', 25: 'Q', 26: 'R',
        27: 'S', 28: 'T', 29: 'U', 30: 'V', 31: 'W', 32: 'X', 33: 'Y', 34: 'Z'
    }

    # Initialize Mediapipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

    # Open webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Unable to access the camera. Please check your camera connection.")
        return

    print("Hand gesture recognition started. Press 'q' to stop.")

    while not stop_detection:
        data_aux = []
        x_ = []
        y_ = []

        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Exiting...")
            break

        H, W, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                    mp.solutions.drawing_styles.get_default_hand_connections_style()
                )

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10
            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10

            # Pad data and make a prediction
            try:
                data_aux_padded = pad_sequences([data_aux], maxlen=42, padding='post', dtype='float32')[0]
                prediction = model.predict([np.asarray(data_aux_padded)])
                predicted_character = labels_dict[int(prediction[0])]

                # Display prediction on the frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                            cv2.LINE_AA)
            except Exception as e:
                print(f"Prediction error: {e}")

        # Show the frame
        cv2.imshow('Hand Gesture Recognition', frame)

        # Break on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Thread wrapper for detect_signs
def start_sign_detection():
    """
    Starts the sign detection in a separate thread.
    """
    detection_thread = threading.Thread(target=detect_signs)
    detection_thread.daemon = True  # Ensures thread exits when the main program exits
    detection_thread.start()

# Function to stop detection
def stop_sign_detection():
    """
    Sets the global flag to stop detection.
    """
    global stop_detection
    stop_detection = True
