from flask import Flask, render_template, Response, jsonify
from handyvision.gesture_detector import classify_gesture
import cv2
import mediapipe as mp

app = Flask(__name__)
last_detected_gesture = "Waiting...."

#camera set up
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

def generate_frames():
    global last_detected_gesture
    while True:
        success, frame = cap.read()
        if not success:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
                # gesture logic here...
                gesture = classify_gesture(handLms)
                last_detected_gesture = gesture
                cv2.putText(frame, gesture, (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/gesture')
def gesture():
    return jsonify({'gesture': last_detected_gesture})

if __name__ == '__main__':
    app.run(debug=True)
