
# Real-Time Tomato Leaf Disease Detection and Smart Monitoring System Using YOLOv8

A computer vision project developed during my summer internship at
the National Institute of Technology Calicut.

The system detects healthy and diseased tomato leaves from live
webcam frames using YOLOv8 and displays the results on an
intelligent monitoring dashboard.

## Key Features

- Real-time tomato leaf disease detection
- Nine classes: one healthy class and eight disease classes
- Bounding boxes, predicted labels and confidence scores
- Disease severity estimates and target coordinates
- Live monitoring of detection counts and FPS
- Automatic CSV logging of detections
- Saving annotated images for later inspection
- Disease-specific management information

## Technology Stack

- Python
- Ultralytics YOLOv8
- OpenCV
- NumPy
- Google Colab
- Roboflow
- Visual Studio Code

## System Workflow

1. Collect and prepare the tomato leaf dataset.
2. Train the YOLOv8 object detection model.
3. Evaluate the trained model.
4. Integrate the model with a webcam application.
5. Display detections and monitoring information.
6. Save detection records for further analysis.

## Dataset

The internship report describes a dataset of nine classes:
Healthy, Bacterial Spot, Early Blight, Late Blight, Leaf Mold,
Mosaic Virus, Septoria Leaf Spot, Spider Mites, and
Yellow Leaf Curl Virus.

## Project Status

The real-time detection and monitoring prototype was developed
as part of the internship.

Autonomous robotic spraying and navigation are future extensions,
not completed features of this repository.

## Future Scope

- Validate the system on diverse real-world field images.
- Explore edge-device deployment.
- Integrate with a robotic spraying system.

## Author

**Banothu Thirupathi**  
B.Tech, Electronics and Communication Engineering  
National Institute of Technology Calicut

