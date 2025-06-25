import math
import mediapipe as mp

# Helper: Euclidean distance between 2 points
def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)

# Main classifier
def classify_gesture(hand_landmarks):
    lm = hand_landmarks.landmark

    # Key landmark references
    thumb_tip = lm[4]
    thumb_ip = lm[3]
    index_tip = lm[8]
    index_pip = lm[6]
    index_mcp = lm[5]
    middle_tip = lm[12]
    middle_mcp = lm[9]
    ring_tip = lm[16]
    ring_pip = lm[14]
    pinky_tip = lm[20]
    pinky_pip = lm[18]
    middle_pip = lm[10]
    

    # --- Gesture Logic ---

    # Thumbs Up
    if (thumb_tip.y < thumb_ip.y and
        index_tip.y > index_mcp.y and
        middle_tip.y > middle_mcp.y):
        return " Thumbs Up"

    # Thumbs Down
    elif (thumb_tip.y > thumb_ip.y and
          index_tip.y > index_mcp.y and
          middle_tip.y > middle_mcp.y):
        return " Thumbs Down"

    # OK Sign (thumb tip and index tip are close)
    elif distance(thumb_tip, index_tip) < 0.05 and \
         middle_tip.y < lm[10].y and \
         ring_tip.y < lm[14].y and \
         pinky_tip.y < lm[18].y:
        return " OK Sign"

    # Open Palm (all fingers extended)
    elif (index_tip.y < index_mcp.y and
          middle_tip.y < middle_mcp.y and
          ring_tip.y < lm[13].y and
          pinky_tip.y < lm[17].y and
          thumb_tip.x < lm[2].x):  # Left hand open outward
        return "Open Palm"
    
    # Middle finger (SYBAU)
    elif(middle_tip.y < middle_pip.y and
        index_tip.y > index_pip.y and
        ring_tip.y > ring_pip.y and
        pinky_tip.y > pinky_pip.y and
        thumb_tip.y > thumb_ip.y):
        return "SYBAU"
    return " Unknown"
