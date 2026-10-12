# ==========================================================
# SMART TOMATO DISEASE DETECTION SYSTEM
# Version 2.1
# Part 1/3
# ==========================================================

from ultralytics import YOLO
import cv2
import numpy as np
import os
import time
from datetime import datetime

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "tomato_detection.pt"
)

# ==========================================================
# LOAD MODEL
# ==========================================================

print("=" * 70)
print("SMART TOMATO DISEASE DETECTION SYSTEM")
print("=" * 70)

print("Loading YOLO model...")

model = YOLO(MODEL_PATH)

print("Model Loaded Successfully!")

# ==========================================================
# DISEASE COLORS
# ==========================================================

DISEASE_COLORS = {

    "Healthy": (0,255,0),

    "Early Blight": (0,165,255),

    "Late Blight": (0,0,255),

    "Leaf Mold": (255,0,0),

    "Leaf Miner": (255,255,0),

    "Mosaic Virus": (255,0,255),

    "Septoria": (0,255,255),

    "Spider Mites": (42,42,165),

    "Yellow Leaf Curl Virus": (203,192,255)

}

# ==========================================================
# DISEASE DATABASE
# ==========================================================

DISEASE_DATABASE = {

    "Healthy":{
        "severity":"None",
        "recommendation":[
            "No treatment required",
            "Continue regular monitoring",
            "Maintain proper irrigation"
        ]
    },

    "Early Blight":{
        "severity":"Medium",
        "recommendation":[
            "Spray Mancozeb",
            "Remove infected leaves",
            "Improve air circulation"
        ]
    },

    "Late Blight":{
        "severity":"High",
        "recommendation":[
            "Spray Metalaxyl + Mancozeb",
            "Remove infected plants",
            "Avoid overhead irrigation"
        ]
    },

    "Leaf Mold":{
        "severity":"Medium",
        "recommendation":[
            "Apply Chlorothalonil",
            "Reduce humidity",
            "Improve ventilation"
        ]
    },

    "Septoria":{
        "severity":"Medium",
        "recommendation":[
            "Spray Mancozeb",
            "Remove infected leaves",
            "Keep foliage dry"
        ]
    },

    "Leaf Miner":{
        "severity":"Low",
        "recommendation":[
            "Use yellow sticky traps",
            "Apply Neem oil",
            "Remove damaged leaves"
        ]
    },

    "Spider Mites":{
        "severity":"Medium",
        "recommendation":[
            "Increase humidity",
            "Apply miticide",
            "Remove infected leaves"
        ]
    },

    "Mosaic Virus":{
        "severity":"High",
        "recommendation":[
            "Remove infected plants",
            "Disinfect tools",
            "Control aphids"
        ]
    },

    "Yellow Leaf Curl Virus":{
        "severity":"High",
        "recommendation":[
            "Control whiteflies",
            "Remove infected plants",
            "Use resistant varieties"
        ]
    }

}

# ==========================================================
# OPEN WEBCAM
# ==========================================================

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():

    print("Cannot open webcam.")

    exit()

print("Webcam Started.")

# ==========================================================
# FPS
# ==========================================================

prev_time = time.time()

# ==========================================================
# MAIN LOOP
# ==========================================================

while True:

    ret, frame = cap.read()

    if not ret:

        break

    # ----------------------------------------
    # YOLO Detection
    # ----------------------------------------

    results = model.predict(

        source=frame,

        imgsz=640,

        conf=0.25,

        verbose=False

    )

    result = results[0]

    detection_count = 0

    # -------------------------------------------------------
    # CURRENT DETECTION
    # This dictionary stores the BEST detection in the frame
    # -------------------------------------------------------

    current_detection = {

        "disease":"None",

        "confidence":0,

        "severity":"None",

        "recommendation":["No Recommendation"],

        "center_x":0,

        "center_y":0

    }



        # ==========================================================
    # PROCESS DETECTIONS
    # ==========================================================

    if result.boxes is not None:

        for box in result.boxes:

            detection_count += 1

            # --------------------------------------
            # Bounding Box
            # --------------------------------------

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            confidence = float(box.conf[0])

            class_id = int(box.cls[0])

            disease = model.names[class_id]

            # --------------------------------------
            # Center Coordinates
            # --------------------------------------

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            # --------------------------------------
            # Get Disease Information
            # --------------------------------------

            disease_info = DISEASE_DATABASE.get(
                disease,
                {
                    "severity": "Unknown",
                    "recommendation": ["No Recommendation"]
                }
            )

            severity = disease_info["severity"]

            recommendation = disease_info["recommendation"]

            # --------------------------------------
            # Save ONLY Highest Confidence Detection
            # --------------------------------------

            if confidence > current_detection["confidence"]:

                current_detection["disease"] = disease

                current_detection["confidence"] = confidence

                current_detection["severity"] = severity

                current_detection["recommendation"] = recommendation

                current_detection["center_x"] = center_x

                current_detection["center_y"] = center_y

            # --------------------------------------
            # Box Color
            # --------------------------------------

            color = DISEASE_COLORS.get(
                disease,
                (255,255,255)
            )

            # --------------------------------------
            # Bounding Box
            # --------------------------------------

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                color,
                2
            )

            # --------------------------------------
            # Label Background
            # --------------------------------------

            (tw, th), _ = cv2.getTextSize(
                f"{disease} {confidence*100:.1f}%",
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                2
            )

            cv2.rectangle(
                frame,
                (x1, y1-32),
                (x1+tw+10, y1),
                color,
                -1
            )

            # --------------------------------------
            # Label
            # --------------------------------------

            cv2.putText(
                frame,
                f"{disease} {confidence*100:.1f}%",
                (x1+5, y1-8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,255),
                2
            )

            # --------------------------------------
            # Center Point
            # --------------------------------------

            cv2.circle(
                frame,
                (center_x, center_y),
                5,
                (0,0,255),
                -1
            )

            # Optional: display center coordinates
            cv2.putText(
                frame,
                f"({center_x},{center_y})",
                (center_x+8, center_y-8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (0,0,255),
                2
            )

    # ==========================================================
    # FPS
    # ==========================================================

    current_time = time.time()

    fps = 1 / (current_time - prev_time)

    prev_time = current_time

    # ==========================================================
    # CURRENT DATE & TIME
    # ==========================================================

    now = datetime.now()

    current_date = now.strftime("%d-%m-%Y")

    current_clock = now.strftime("%I:%M:%S %p")

        # ==========================================================
    # CREATE DASHBOARD
    # ==========================================================

    dashboard_width = 380

    height, width = frame.shape[:2]

    dashboard = np.ones(
        (height, dashboard_width, 3),
        dtype=np.uint8
    ) * 255

    # ==========================================================
    # TITLE
    # ==========================================================

    cv2.putText(
        dashboard,
        "SMART TOMATO",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0,0,255),
        2
    )

    cv2.putText(
        dashboard,
        "DISEASE DETECTION",
        (20,75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,0,255),
        2
    )

    cv2.putText(
        dashboard,
        "SYSTEM",
        (20,105),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,0,255),
        2
    )

    cv2.line(
        dashboard,
        (15,125),
        (360,125),
        (100,100,100),
        2
    )

    # ==========================================================
    # DISEASE INFORMATION
    # ==========================================================

    cv2.putText(
        dashboard,
        "Disease",
        (20,165),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255,0,0),
        2
    )

    cv2.putText(
        dashboard,
        current_detection["disease"],
        (170,165),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0,0,0),
        2
    )

    cv2.putText(
        dashboard,
        "Confidence",
        (20,205),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255,0,0),
        2
    )

    cv2.putText(
        dashboard,
        f"{current_detection['confidence']*100:.1f}%",
        (170,205),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0,0,0),
        2
    )

    cv2.putText(
        dashboard,
        "Severity",
        (20,245),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255,0,0),
        2
    )

    cv2.putText(
        dashboard,
        current_detection["severity"],
        (170,245),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0,0,255),
        2
    )

    # ==========================================================
    # RECOMMENDATION
    # ==========================================================

    cv2.line(
        dashboard,
        (15,270),
        (360,270),
        (180,180,180),
        1
    )

    cv2.putText(
        dashboard,
        "Recommendation",
        (20,300),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0,120,255),
        2
    )

    y = 335

    for rec in current_detection["recommendation"]:

        cv2.putText(
            dashboard,
            "-- " + rec,
            (25,y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0,0,0),
            2
        )

        y += 30

    # ==========================================================
    # SYSTEM INFORMATION
    # ==========================================================

    cv2.line(
        dashboard,
        (15,440),
        (360,440),
        (180,180,180),
        1
    )

    info = [

        ("Center X", current_detection["center_x"]),

        ("Center Y", current_detection["center_y"]),

        ("Detections", detection_count),

        ("FPS", f"{fps:.2f}"),

        ("Date", current_date),

        ("Time", current_clock)

    ]

    y = 475

    for key, value in info:

        cv2.putText(
            dashboard,
            f"{key} : {value}",
            (20,y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.58,
            (0,0,0),
            2
        )

        y += 35

    # ==========================================================
    # COMBINE CAMERA + DASHBOARD
    # ==========================================================

    combined = np.hstack((frame, dashboard))

    cv2.imshow(
        "Smart Tomato Disease Detection System",
        combined
    )

    # ==========================================================
    # EXIT
    # ==========================================================

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q') or key == ord('Q'):
        break


# ==========================================================
# CLEANUP
# ==========================================================

cap.release()

cv2.destroyAllWindows()

print("\nApplication Closed Successfully.")