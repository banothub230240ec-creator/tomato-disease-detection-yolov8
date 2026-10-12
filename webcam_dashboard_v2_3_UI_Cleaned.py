# ==========================================================
# SMART TOMATO DISEASE DETECTION SYSTEM
# Version : 2.3
# ==========================================================
#
# Developed By :
# Banothu Thirupathi
#
# Features
# ----------------------------------------------------------
# ✓ Real-Time Tomato Disease Detection
# ✓ YOLOv8 Object Detection
# ✓ Robot Target Lock
# ✓ Disease Recommendation System
# ✓ Professional Dashboard
# ✓ Automatic Image Saving
# ✓ CSV Detection Logging
# ✓ Robot Command Module
# ✓ Session Statistics
#
# Future Versions
# ----------------------------------------------------------
# ✓ ROS2 Integration
# ✓ Gazebo Simulation
# ✓ Autonomous Robot Navigation
# ✓ Robotic Arm Spraying
# ==========================================================

# ==========================================================
# IMPORT LIBRARIES
# ==========================================================

from ultralytics import YOLO

import cv2
import numpy as np

import os
import csv
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

RESULTS_FOLDER = os.path.join(
    BASE_DIR,
    "results"
)

IMAGE_FOLDER = os.path.join(
    RESULTS_FOLDER,
    "images"
)

LOG_FOLDER = os.path.join(
    RESULTS_FOLDER,
    "logs"
)

CSV_FILE = os.path.join(
    LOG_FOLDER,
    "detection_log.csv"
)

# ==========================================================
# CREATE DIRECTORIES
# ==========================================================

os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

# ==========================================================
# APPLICATION SETTINGS
# ==========================================================

CONFIDENCE_THRESHOLD = 0.25

IMAGE_SIZE = 640

WINDOW_NAME = "Smart Tomato Disease Detection System"

DASHBOARD_WIDTH = 700

FONT = cv2.FONT_HERSHEY_SIMPLEX

FONT_SCALE = 0.60

LINE_THICKNESS = 2

# ==========================================================
# LOAD MODEL
# ==========================================================

print("=" * 70)
print("SMART TOMATO DISEASE DETECTION SYSTEM")
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

    "None": (0,200,0),

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

    "TARGET LOCKED": (0,200,0),

    "READY": (255,0,0),

    "SPRAYING": (255,0,255)

}

print("Configuration Loaded Successfully.")













#PART 2



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
            "Reduce humidity",
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
            "Use Yellow Sticky Traps",
            "Apply Neem Oil",
            "Remove Damaged Leaves"
        ]
    },

    "Spider Mites": {
        "severity": "Medium",
        "recommendation": [
            "Increase Humidity",
            "Apply Suitable Miticide",
            "Remove Infected Leaves"
        ]
    },

    "Mosaic Virus": {
        "severity": "High",
        "recommendation": [
            "Remove Infected Plants",
            "Disinfect Farming Tools",
            "Control Aphids"
        ]
    },

    "Yellow Leaf Curl Virus": {
        "severity": "High",
        "recommendation": [
            "Control Whiteflies",
            "Remove Infected Plants",
            "Use Resistant Varieties"
        ]
    }

}

print("Disease Database Loaded Successfully.")

# ==========================================================
# CREATE CSV FILE
# ==========================================================

if not os.path.exists(CSV_FILE):

    with open(CSV_FILE, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Date",
            "Time",
            "Disease",
            "Confidence",
            "Target X",
            "Target Y"
        ])

print("CSV Logger Ready.")

# ==========================================================
# ROBOT TARGET
# ==========================================================

robot_target = {

    "locked": False,

    "disease": "None",

    "confidence": 0.0,

    "severity": "Unknown",

    "recommendation": [

        "Searching..."

    ],

    "target_x": 0,

    "target_y": 0

}

# ==========================================================
# ROBOT COMMAND
# ==========================================================

robot_command = {

    "status": "SEARCHING",

    "target_locked": False,

    "disease": "None",

    "confidence": 0.0,

    "target_x": 0,

    "target_y": 0,

    "spray": False

}

# ==========================================================
# SESSION STATISTICS
# ==========================================================

session_stats = {

    "frames": 0,

    "detections": 0,

    "healthy": 0,

    "diseased": 0,

    "images_saved": 0

}

# ==========================================================
# DISEASE COUNTERS
# ==========================================================

disease_counter = {

    "Healthy": 0,

    "Early Blight": 0,

    "Late Blight": 0,

    "Leaf Mold": 0,

    "Septoria": 0,

    "Leaf Miner": 0,

    "Spider Mites": 0,

    "Mosaic Virus": 0,

    "Yellow Leaf Curl Virus": 0

}

# ==========================================================
# LAST LOGGED TARGET
# ==========================================================

last_logged = {

    "disease": None,

    "x": -100,

    "y": -100

}

print("Robot Modules Initialized.")

print("=" * 70)








#PART 3




# ==========================================================
# OPEN WEBCAM
# ==========================================================

print("\nOpening Webcam...")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Full HD Resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():

    print("ERROR : Unable to access webcam.")

    exit()

print("Webcam Started Successfully!")

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"Resolution : {frame_width} x {frame_height}")

print("=" * 70)

# ==========================================================
# FPS TIMER
# ==========================================================

previous_time = time.time()

# ==========================================================
# START APPLICATION
# ==========================================================

print("\nStarting Smart Tomato Disease Detection...\n")

# ==========================================================
# MAIN LOOP
# ==========================================================

while True:

    # ------------------------------------------------------
    # Read Frame
    # ------------------------------------------------------

    ret, frame = cap.read()

    if not ret:

        print("Failed to capture frame.")

        break

    # ------------------------------------------------------
    # Session Statistics
    # ------------------------------------------------------

    session_stats["frames"] += 1

    detection_count = 0

    # ------------------------------------------------------
    # Reset Robot Target
    # ------------------------------------------------------

    robot_target["locked"] = False

    robot_target["disease"] = "None"

    robot_target["confidence"] = 0.0

    robot_target["severity"] = "Unknown"

    robot_target["recommendation"] = [
        "Searching for diseased leaf..."
    ]

    robot_target["target_x"] = 0

    robot_target["target_y"] = 0

    # ------------------------------------------------------
    # Date & Time
    # ------------------------------------------------------

    now = datetime.now()

    current_date = now.strftime("%d-%m-%Y")

    current_time_text = now.strftime("%I:%M:%S %p")

    # ------------------------------------------------------
    # Dashboard Canvas
    # ------------------------------------------------------

    dashboard = np.ones(

        (frame_height, DASHBOARD_WIDTH, 3),

        dtype=np.uint8

    ) * 255

    # ------------------------------------------------------
    # Dashboard Header
    # ------------------------------------------------------

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

        "DISEASE DETECTION SYSTEM",

        (20, 70),

        FONT,

        0.70,

        (0,255,255),

        2

    )






#PART 4

    # ==========================================================
    # YOLOv8 DISEASE DETECTION
    # ==========================================================

    results = model.predict(

        source=frame,

        imgsz=IMAGE_SIZE,

        conf=CONFIDENCE_THRESHOLD,

        verbose=False

    )

    result = results[0]

    # ==========================================================
    # PROCESS DETECTIONS
    # ==========================================================

    if result.boxes is not None:

        for box in result.boxes:

            detection_count += 1

            session_stats["detections"] += 1

            # --------------------------------------------------
            # Bounding Box Coordinates
            # --------------------------------------------------

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            confidence = float(box.conf[0])

            class_id = int(box.cls[0])

            disease = model.names[class_id]

            # --------------------------------------------------
            # Center Coordinates
            # --------------------------------------------------

            center_x = (x1 + x2) // 2

            center_y = (y1 + y2) // 2

            # --------------------------------------------------
            # Disease Information
            # --------------------------------------------------

            disease_info = DISEASE_DATABASE.get(

                disease,

                {

                    "severity": "Unknown",

                    "recommendation": [

                        "No Recommendation Available"

                    ]

                }

            )

            severity = disease_info["severity"]

            recommendation = disease_info["recommendation"]

            # --------------------------------------------------
            # Disease Counter
            # --------------------------------------------------

            if disease in disease_counter:

                disease_counter[disease] += 1

            if disease == "Healthy":

                session_stats["healthy"] += 1

            else:

                session_stats["diseased"] += 1

            # --------------------------------------------------
            # ROBOT TARGET LOCK
            # --------------------------------------------------

            if confidence > robot_target["confidence"]:

                robot_target["locked"] = True

                robot_target["disease"] = disease

                robot_target["confidence"] = confidence

                robot_target["severity"] = severity

                robot_target["recommendation"] = recommendation

                robot_target["target_x"] = center_x

                robot_target["target_y"] = center_y

            # --------------------------------------------------
            # ROBOT COMMAND
            # --------------------------------------------------

            robot_command["status"] = "TARGET LOCKED"

            robot_command["target_locked"] = True

            robot_command["disease"] = disease

            robot_command["confidence"] = confidence

            robot_command["target_x"] = center_x

            robot_command["target_y"] = center_y

            robot_command["spray"] = False

            # --------------------------------------------------
            # CSV LOGGER
            # --------------------------------------------------

            if (

                disease != last_logged["disease"]

                or

                abs(center_x - last_logged["x"]) > 30

                or

                abs(center_y - last_logged["y"]) > 30

            ):

                with open(CSV_FILE, "a", newline="") as file:

                    writer = csv.writer(file)

                    writer.writerow([

                        current_date,

                        current_time_text,

                        disease,

                        round(confidence * 100, 2),

                        center_x,

                        center_y

                    ])

                last_logged["disease"] = disease

                last_logged["x"] = center_x

                last_logged["y"] = center_y

            # --------------------------------------------------
            # Bounding Box Color
            # --------------------------------------------------

            color = DISEASE_COLORS.get(

                disease,

                (255,255,255)

            )

            # --------------------------------------------------
            # Draw Bounding Box
            # --------------------------------------------------

            cv2.rectangle(

                frame,

                (x1, y1),

                (x2, y2),

                color,

                2

            )

            # --------------------------------------------------
            # Draw Label
            # --------------------------------------------------

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

            cv2.putText(

                frame,

                label,

                (x1+5, y1-8),

                FONT,

                0.6,

                (255,255,255),

                2

            )

            # --------------------------------------------------
            # Center Point
            # --------------------------------------------------

            cv2.circle(

                frame,

                (center_x, center_y),

                5,

                (0,0,255),

                -1

            )

            # --------------------------------------------------
            # Target Lock Indicator
            # --------------------------------------------------

            if (

                center_x == robot_target["target_x"]

                and

                center_y == robot_target["target_y"]

            ):

                cv2.circle(

                    frame,

                    (center_x, center_y),

                    20,

                    (0,255,255),

                    2

                )

                cv2.putText(

                    frame,

                    "TARGET",

                    (center_x-35, center_y-25),

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

    # ==========================================================
    # FPS CALCULATION
    # ==========================================================

    current_time = time.time()

    fps = 1 / (current_time - previous_time)

    previous_time = current_time


        # ==========================================================
    # DASHBOARD
    # ==========================================================

    # Background
    dashboard[:] = (250, 250, 250)

    # Header
    cv2.rectangle(
        dashboard,
        (0, 0),
        (DASHBOARD_WIDTH, 110),
        (45, 45, 45),
        -1
    )

    cv2.putText(
        dashboard,
        "SMART TOMATO",
        (25, 55),
        FONT,
        1.25,
        (255,255,255),
        2
    )

    cv2.putText(
        dashboard,
        "DISEASE DETECTION",
        (25, 110),
        FONT,
        0.95,
        (0,255,255),
        2
    )

    # ----------------------------------------------------------
    # Robot Status
    # ----------------------------------------------------------

    if robot_target["locked"]:

        status = "TARGET LOCKED"

        status_color = (0,180,0)

    else:

        status = "SEARCHING"

        status_color = (0,0,255)

    cv2.putText(
        dashboard,
        "Robot Status",
        (25,150),
        FONT,
        0.7,
        (0,0,0),
        2
    )

    cv2.putText(
        dashboard,
        status,
        (360,150),
        FONT,
        0.7,
        status_color,
        2
    )

    cv2.line(
        dashboard,
        (20,175),
        (680,175),
        (180,180,180),
        1
    )

    # ----------------------------------------------------------
    # Disease Information
    # ----------------------------------------------------------

    cv2.putText(
        dashboard,
        "Disease",
        (25,230),
        FONT,
        0.75,
        (255,0,0),
        2
    )

    cv2.putText(
        dashboard,
        robot_target["disease"],
        (360,230),
        FONT,
        0.75,
        (0,0,0),
        2
    )

    cv2.putText(
        dashboard,
        "Confidence",
        (25,290),
        FONT,
        0.75,
        (255,0,0),
        2
    )

    cv2.putText(
        dashboard,
        f"{robot_target['confidence']*100:.1f}%",
        (360,290),
        FONT,
        0.75,
        (0,0,0),
        2
    )

    cv2.putText(
        dashboard,
        "Severity",
        (25,350),
        FONT,
        0.75,
        (255,0,0),
        2
    )

    severity_color = SEVERITY_COLORS.get(
        robot_target["severity"],
        (0,0,0)
    )

    cv2.putText(
        dashboard,
        robot_target["severity"],
        (360,350),
        FONT,
        0.75,
        severity_color,
        2
    )

    cv2.line(
        dashboard,
        (20,390),
        (680,390),
        (180,180,180),
        1
    )


    #PART 5B





        # ==========================================================
    # RECOMMENDATION PANEL
    # ==========================================================

    cv2.putText(

        dashboard,

        "SMART RECOMMENDATION",

        (25,430),

        FONT,

        0.80,

        (0,140,255),

        2

    )

    cv2.putText(
        dashboard,
        "RECOMMENDED TREATMENT",
        (30,480),
        FONT,
        0.70,
        (0,140,255),
        2
    )

    y_position = 525

    for rec in robot_target["recommendation"]:

        cv2.putText(
            dashboard,
            "- " + rec,
            (45,y_position),
            FONT,
            0.58,
            (0,0,0),
            2
        )
        y_position += 35

    cv2.putText(
        dashboard,"PREVENTION",(30,650),FONT,0.70,(0,140,255),2)

    cv2.putText(
        dashboard,
        "- Regular field monitoring",
        (45,690),
        FONT,
        0.55,
        (0,0,0),
        2
    )

    cv2.putText(
        dashboard,
        "- Remove infected leaves",
        (45,725),
        FONT,
        0.55,
        (0,0,0),
        2
    )

    cv2.line(

        dashboard,

        (20,770),

        (680,770),

        (180,180,180),

        1

    )

    # ==========================================================
    # TARGET INFORMATION
    # ==========================================================

    cv2.putText(

        dashboard,

        "Target X",

        (25,815),

        FONT,

        0.75,

        (255,0,0),

        2

    )

    cv2.putText(

        dashboard,

        str(robot_target["target_x"]),

        (360,815),

        FONT,

        0.75,

        (0,0,255),

        2

    )

    cv2.putText(

        dashboard,

        "Target Y",

        (25,860),

        FONT,

        0.75,

        (255,0,0),

        2

    )

    cv2.putText(

        dashboard,

        str(robot_target["target_y"]),

        (360,860),

        FONT,

        0.75,

        (0,0,255),

        2

    )

    cv2.putText(

        dashboard,

        "Detections",

        (25,905),

        FONT,

        0.75,

        (255,0,0),

        2

    )

    cv2.putText(

        dashboard,

        str(detection_count),

        (360,905),

        FONT,

        0.75,

        (0,150,0),

        2

    )

    cv2.line(

        dashboard,

        (20,950),

        (680,950),

        (180,180,180),

        1

    )

    # ==========================================================
    # SYSTEM INFORMATION
    # ==========================================================

    cv2.putText(

        dashboard,

        "FPS",

        (25,990),

        FONT,

        0.75,

        (255,0,0),

        2

    )

    cv2.putText(

        dashboard,

        f"{fps:.2f}",

        (360,990),

        FONT,

        0.75,

        (0,0,0),

        2

    )

    cv2.putText(

        dashboard,

        "Date",

        (25,1030),

        FONT,

        0.75,

        (255,0,0),

        2

    )

    cv2.putText(

        dashboard,

        current_date,

        (360,1030),

        FONT,

        0.75,

        (0,0,0),

        2

    )

    cv2.putText(

        dashboard,

        "Time",

        (25,1070),

        FONT,

        0.75,

        (255,0,0),

        2

    )

    cv2.putText(

        dashboard,

        current_time_text,

        (360,1070),

        FONT,

        0.65,

        (0,0,0),

        2

    )

    cv2.putText(

        dashboard,

        "Press S : Save Image",

        (25,1110),

        FONT,

        0.60,

        (100,100,100),

        2

    )

    cv2.putText(

        dashboard,

        "Press Q : Exit",

        (390,1110),

        FONT,

        0.60,

        (100,100,100),

        2

    )



    #PART 5C


        # ==========================================================
    # COMBINE CAMERA + DASHBOARD
    # ==========================================================

    camera_width = 1220
    camera_height = 1080
    frame = cv2.resize(frame, (camera_width, camera_height))

    combined_frame = np.hstack(

        (

            frame,

            dashboard

        )

    )

    # ==========================================================
    # DISPLAY WINDOW
    # ==========================================================

    cv2.namedWindow(

        WINDOW_NAME,

        cv2.WINDOW_NORMAL

    )

    cv2.imshow(

        WINDOW_NAME,

        combined_frame

    )

    # ==========================================================
    # KEYBOARD CONTROLS
    # ==========================================================

    key = cv2.waitKey(1) & 0xFF

    # ----------------------------------------------------------
    # SAVE IMAGE
    # ----------------------------------------------------------

    if key == ord("s"):

        timestamp = datetime.now().strftime(

            "%Y%m%d_%H%M%S"

        )

        filename = (

            f"{robot_target['disease'].replace(' ','_')}_"

            f"{timestamp}.jpg"

        )

        save_path = os.path.join(

            IMAGE_FOLDER,

            filename

        )

        cv2.imwrite(

            save_path,

            combined_frame

        )

        session_stats["images_saved"] += 1

        print("=" * 70)

        print("IMAGE SAVED SUCCESSFULLY")

        print(save_path)

        print("=" * 70)

    # ----------------------------------------------------------
    # QUIT PROGRAM
    # ----------------------------------------------------------

    if key == ord("q"):

        print("\nClosing Smart Tomato Disease Detection System...")

        break










