# ==========================================================
# SMART TOMATO DISEASE DETECTION SYSTEM
# ----------------------------------------------------------
# Version : 2.2
#
# Developed By:
# Banothu Thirupathi
#
# Features
# ----------------------------------------------------------
# ✓ Real-Time Tomato Disease Detection
# ✓ YOLOv8 Object Detection
# ✓ Robot Target Lock
# ✓ AI Recommendation System
# ✓ Disease Severity Analysis
# ✓ Professional Dashboard
# ✓ FPS Counter
# ✓ Target Coordinates
# ✓ Robot Status
#
# Future Features
# ----------------------------------------------------------
# ✓ CSV Detection Logger
# ✓ Save Detection Images
# ✓ ROS2 Integration
# ✓ Gazebo Integration
# ✓ Robotic Arm Spraying
# ==========================================================

# ==========================================================
# IMPORT LIBRARIES
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

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "tomato_detection.pt"
)

# ==========================================================
# APPLICATION SETTINGS
# ==========================================================

CONFIDENCE_THRESHOLD = 0.25

IMAGE_SIZE = 640

WINDOW_NAME = "Smart Tomato Disease Detection System"

DASHBOARD_WIDTH = 520

FONT = cv2.FONT_HERSHEY_SIMPLEX

# ==========================================================
# LOAD YOLO MODEL
# ==========================================================

print("=" * 70)
print(" SMART TOMATO DISEASE DETECTION SYSTEM ")
print("=" * 70)

print("\nLoading YOLOv8 Model...")

model = YOLO(MODEL_PATH)

print("Model Loaded Successfully!")

print("=" * 70)

# ==========================================================
# DISEASE COLORS
# ==========================================================

DISEASE_COLORS = {

    "Healthy": (0,255,0),

    "Early Blight": (0,165,255),

    "Late Blight": (0,0,255),

    "Leaf Mold": (255,0,0),

    "Septoria": (0,255,255),

    "Leaf Miner": (255,255,0),

    "Spider Mites": (128,0,128),

    "Mosaic Virus": (255,0,255),

    "Yellow Leaf Curl Virus": (180,105,255)

}

# ==========================================================
# SEVERITY COLORS
# ==========================================================

SEVERITY_COLORS = {

    "None": (0,180,0),

    "Low": (0,200,0),

    "Medium": (0,165,255),

    "High": (0,0,255),

    "Unknown": (120,120,120)

}

# ==========================================================
# ROBOT STATUS COLORS
# ==========================================================

STATUS_COLORS = {

    "SEARCHING": (0,0,255),

    "TARGET LOCKED": (0,180,0),

    "READY": (255,0,0),

    "SPRAYING": (255,0,255)

}

print("Configuration Loaded Successfully.")



#part 2

# ==========================================================
# DISEASE DATABASE
# ==========================================================

DISEASE_DATABASE = {

    "Healthy": {
        "severity": "None",
        "recommendation": [
            "No treatment required",
            "Continue regular monitoring",
            "Maintain proper irrigation"
        ]
    },

    "Early Blight": {
        "severity": "Medium",
        "recommendation": [
            "Spray Mancozeb fungicide",
            "Remove infected leaves",
            "Improve air circulation"
        ]
    },

    "Late Blight": {
        "severity": "High",
        "recommendation": [
            "Spray Metalaxyl + Mancozeb",
            "Remove infected plants",
            "Avoid overhead irrigation"
        ]
    },

    "Leaf Mold": {
        "severity": "Medium",
        "recommendation": [
            "Apply Chlorothalonil",
            "Reduce greenhouse humidity",
            "Increase ventilation"
        ]
    },

    "Septoria": {
        "severity": "Medium",
        "recommendation": [
            "Spray Mancozeb",
            "Remove infected leaves",
            "Keep foliage dry"
        ]
    },

    "Leaf Miner": {
        "severity": "Low",
        "recommendation": [
            "Use yellow sticky traps",
            "Apply Neem oil",
            "Remove damaged leaves"
        ]
    },

    "Spider Mites": {
        "severity": "Medium",
        "recommendation": [
            "Increase humidity",
            "Apply suitable miticide",
            "Remove infected leaves"
        ]
    },

    "Mosaic Virus": {
        "severity": "High",
        "recommendation": [
            "Remove infected plants",
            "Disinfect farming tools",
            "Control aphids immediately"
        ]
    },

    "Yellow Leaf Curl Virus": {
        "severity": "High",
        "recommendation": [
            "Control whiteflies",
            "Remove infected plants",
            "Use resistant tomato varieties"
        ]
    }

}

print("Disease Database Loaded.")

# ==========================================================
# OPEN WEBCAM
# ==========================================================

print("\nOpening Webcam...")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():

    print("ERROR : Unable to access webcam.")

    exit()

print("Webcam Started Successfully.")

# ==========================================================
# FRAME INFORMATION
# ==========================================================

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"Resolution : {frame_width} x {frame_height}")

# ==========================================================
# FPS TIMER
# ==========================================================

prev_time = time.time()

# ==========================================================
# MAIN PROGRAM
# ==========================================================

print("\nStarting Smart Detection...\n")

while True:

    ret, frame = cap.read()

    if not ret:

        print("Unable to capture frame.")

        break

    # ======================================================
    # ROBOT TARGET OBJECT
    # ======================================================

    robot_target = {

        "locked": False,

        "disease": "None",

        "confidence": 0.0,

        "severity": "Unknown",

        "recommendation": [

            "Searching for disease..."

        ],

        "target_x": 0,

        "target_y": 0

    }

    detection_count = 0

    # ======================================================
    # CURRENT DATE & TIME
    # ======================================================

    now = datetime.now()

    current_date = now.strftime("%d-%m-%Y")

    current_clock = now.strftime("%I:%M:%S %p")




#Part 3


    # ======================================================
    # YOLO DETECTION
    # ======================================================

    results = model.predict(

        source=frame,

        imgsz=IMAGE_SIZE,

        conf=CONFIDENCE_THRESHOLD,

        verbose=False

    )

    result = results[0]

    # ======================================================
    # PROCESS DETECTIONS
    # ======================================================

    if result.boxes is not None:

        for box in result.boxes:

            detection_count += 1

            # ---------------------------------------------
            # Bounding Box Coordinates
            # ---------------------------------------------

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            confidence = float(box.conf[0])

            class_id = int(box.cls[0])

            disease = model.names[class_id]

            # ---------------------------------------------
            # Center Coordinates
            # ---------------------------------------------

            center_x = int((x1 + x2) / 2)

            center_y = int((y1 + y2) / 2)

            # ---------------------------------------------
            # Disease Information
            # ---------------------------------------------

            disease_info = DISEASE_DATABASE.get(

                disease,

                {

                    "severity": "Unknown",

                    "recommendation": [

                        "No recommendation available"

                    ]

                }

            )

            severity = disease_info["severity"]

            recommendations = disease_info["recommendation"]

            # ---------------------------------------------
            # Robot Target Selection
            # ---------------------------------------------

            if confidence > robot_target["confidence"]:

                robot_target["locked"] = True

                robot_target["disease"] = disease

                robot_target["confidence"] = confidence

                robot_target["severity"] = severity

                robot_target["recommendation"] = recommendations

                robot_target["target_x"] = center_x

                robot_target["target_y"] = center_y

            # ---------------------------------------------
            # Bounding Box Color
            # ---------------------------------------------

            color = DISEASE_COLORS.get(

                disease,

                (255,255,255)

            )

            # ---------------------------------------------
            # Draw Bounding Box
            # ---------------------------------------------

            cv2.rectangle(

                frame,

                (x1, y1),

                (x2, y2),

                color,

                2

            )

            # ---------------------------------------------
            # Draw Label Background
            # ---------------------------------------------

            label = f"{disease} {confidence*100:.1f}%"

            (tw, th), _ = cv2.getTextSize(

                label,

                FONT,

                0.6,

                2

            )

            cv2.rectangle(

                frame,

                (x1, y1-30),

                (x1+tw+10, y1),

                color,

                -1

            )

            # ---------------------------------------------
            # Disease Label
            # ---------------------------------------------

            cv2.putText(

                frame,

                label,

                (x1+5, y1-8),

                FONT,

                0.6,

                (255,255,255),

                2

            )

            # ---------------------------------------------
            # Center Point
            # ---------------------------------------------

            cv2.circle(

                frame,

                (center_x, center_y),

                5,

                (0,0,255),

                -1

            )

            # ---------------------------------------------
            # Target Lock Highlight
            # ---------------------------------------------

            if (

                robot_target["locked"]

                and

                center_x == robot_target["target_x"]

                and

                center_y == robot_target["target_y"]

            ):

                cv2.circle(

                    frame,

                    (center_x, center_y),

                    18,

                    (0,255,255),

                    2

                )

                cv2.putText(

                    frame,

                    "TARGET",

                    (center_x-30, center_y-25),

                    FONT,

                    0.55,

                    (0,255,255),

                    2

                )

                cv2.line(

                    frame,

                    (center_x-20, center_y),

                    (center_x+20, center_y),

                    (0,255,255),

                    1

                )

                cv2.line(

                    frame,

                    (center_x, center_y-20),

                    (center_x, center_y+20),

                    (0,255,255),

                    1

                )

    # ======================================================
    # FPS CALCULATION
    # ======================================================

    current_time = time.time()

    fps = 1 / (current_time - prev_time)

    prev_time = current_time



    #part 4

        # ======================================================
    # CREATE DASHBOARD
    # ======================================================

    dashboard = np.ones(

        (frame_height, DASHBOARD_WIDTH, 3),

        dtype=np.uint8

    ) * 255

    # ======================================================
    # HEADER
    # ======================================================

    cv2.rectangle(

        dashboard,

        (0, 0),

        (DASHBOARD_WIDTH, 90),

        (45, 45, 45),

        -1

    )

    cv2.putText(

        dashboard,

        "SMART TOMATO",

        (20, 35),

        FONT,

        0.9,

        (255,255,255),

        2

    )

    cv2.putText(

        dashboard,

        "DISEASE DETECTION",

        (20, 65),

        FONT,

        0.70,

        (0,255,255),

        2

    )

    # ======================================================
    # ROBOT STATUS
    # ======================================================

    if robot_target["locked"]:

        robot_status = "TARGET LOCKED"

    else:

        robot_status = "SEARCHING"

    status_color = STATUS_COLORS.get(

        robot_status,

        (0,0,0)

    )

    cv2.putText(

        dashboard,

        "Robot Status",

        (20,120),

        FONT,

        0.60,

        (0,0,0),

        2

    )

    cv2.putText(

        dashboard,

        robot_status,

        (180,120),

        FONT,

        0.60,

        status_color,

        2

    )

    cv2.line(

        dashboard,

        (15,140),

        (365,140),

        (180,180,180),

        1

    )

    # ======================================================
    # TARGET INFORMATION
    # ======================================================

    disease_color = DISEASE_COLORS.get(

        robot_target["disease"],

        (0,0,0)

    )

    severity_color = SEVERITY_COLORS.get(

        robot_target["severity"],

        (0,0,0)

    )

    cv2.putText(

        dashboard,

        "Target Disease",

        (20,175),

        FONT,

        0.60,

        (0,0,0),

        2

    )

    cv2.putText(

        dashboard,

        robot_target["disease"],

        (180,175),

        FONT,

        0.60,

        disease_color,

        2

    )

    cv2.putText(

        dashboard,

        "Confidence",

        (20,210),

        FONT,

        0.60,

        (0,0,0),

        2

    )

    cv2.putText(

        dashboard,

        f"{robot_target['confidence']*100:.1f}%",

        (180,210),

        FONT,

        0.60,

        (0,0,0),

        2

    )

    cv2.putText(

        dashboard,

        "Severity",

        (20,245),

        FONT,

        0.60,

        (0,0,0),

        2

    )

    cv2.putText(

        dashboard,

        robot_target["severity"],

        (180,245),

        FONT,

        0.60,

        severity_color,

        2

    )

    cv2.line(

        dashboard,

        (15,265),

        (365,265),

        (180,180,180),

        1

    )

    # ======================================================
    # RECOMMENDATIONS
    # ======================================================

    cv2.putText(

        dashboard,

        "Recommendation",

        (20,295),

        FONT,

        0.65,

        (255,0,0),

        2

    )

    y = 330

    for rec in robot_target["recommendation"]:

        cv2.putText(

            dashboard,

            "- " + rec,

            (30, y),

            FONT,

            0.50,

            (0,0,0),

            2

        )

        y += 28

    # ======================================================
    # TARGET COORDINATES
    # ======================================================

    cv2.line(

        dashboard,

        (15,430),

        (365,430),

        (180,180,180),

        1

    )

    cv2.putText(

        dashboard,

        "Target X",

        (20,460),

        FONT,

        0.60,

        (0,0,0),

        2

    )

    cv2.putText(

        dashboard,

        str(robot_target["target_x"]),

        (180,460),

        FONT,

        0.60,

        (0,0,255),

        2

    )

    cv2.putText(

        dashboard,

        "Target Y",

        (20,495),

        FONT,

        0.60,

        (0,0,0),

        2

    )

    cv2.putText(

        dashboard,

        str(robot_target["target_y"]),

        (180,495),

        FONT,

        0.60,

        (0,0,255),

        2

    )

    cv2.putText(

        dashboard,

        "Detections",

        (20,530),

        FONT,

        0.60,

        (0,0,0),

        2

    )

    cv2.putText(

        dashboard,

        str(detection_count),

        (180,530),

        FONT,

        0.60,

        (0,0,255),

        2

    )

    # ======================================================
    # SYSTEM INFORMATION
    # ======================================================

    cv2.line(

        dashboard,

        (15,555),

        (365,555),

        (180,180,180),

        1

    )

    cv2.putText(

        dashboard,

        f"FPS : {fps:.2f}",

        (20,585),

        FONT,

        0.60,

        (0,150,0),

        2

    )

    cv2.putText(

        dashboard,

        current_date,

        (20,620),

        FONT,

        0.55,

        (0,0,0),

        2

    )

    cv2.putText(

        dashboard,

        current_clock,

        (20,650),

        FONT,

        0.55,

        (0,0,0),

        2

    )




    #part 5

        # ======================================================
    # CREATE RESULTS DIRECTORY
    # ======================================================

    results_folder = os.path.join(

        BASE_DIR,

        "results"

    )

    images_folder = os.path.join(

        results_folder,

        "images"

    )

    os.makedirs(

        images_folder,

        exist_ok=True

    )

    # ======================================================
    # COMBINE CAMERA + DASHBOARD
    # ======================================================

    combined_frame = np.hstack((frame, dashboard))

    cv2.namedWindow(
        WINDOW_NAME,
        cv2.WINDOW_NORMAL
    )

    cv2.imshow(
        WINDOW_NAME,
        combined_frame
    )

    # ======================================================
    # KEYBOARD CONTROLS
    # ======================================================

    key = cv2.waitKey(1) & 0xFF

    # ------------------------------------------------------
    # Save Current Detection
    # ------------------------------------------------------

    if key == ord("s"):

        timestamp = datetime.now().strftime(

            "%Y%m%d_%H%M%S"

        )

        filename = f"Detection_{timestamp}.jpg"

        save_path = os.path.join(

            images_folder,

            filename

        )

        cv2.imwrite(

            save_path,

            combined_frame

        )

        print("=" * 60)

        print("Detection Image Saved Successfully")

        print(save_path)

        print("=" * 60)

    # ------------------------------------------------------
    # Quit Program
    # ------------------------------------------------------

    if key == ord("q"):

        print("\nClosing Application...")

        break