from ultralytics import YOLO
import cv2
import os

# ============================
# Paths
# ============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "tomato_detection.pt")
IMAGE_FOLDER = os.path.join(BASE_DIR, "test_images")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "results")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ============================
# Load Model
# ============================

model = YOLO(MODEL_PATH)

print("\nModel Loaded Successfully!")
print("Classes:", model.names)

# ============================
# Supported Image Formats
# ============================

extensions = (".jpg", ".jpeg", ".png", ".webp")

images = [
    f for f in os.listdir(IMAGE_FOLDER)
    if f.lower().endswith(extensions)
]

print(f"\nFound {len(images)} images.\n")

# ============================
# Process Images
# ============================

for image_name in images:

    image_path = os.path.join(IMAGE_FOLDER, image_name)

    results = model.predict(
        source=image_path,
        imgsz=640,
        conf=0.25,
        save=False,
        verbose=False
    )

    result = results[0]

    # Draw predictions
    annotated = result.plot()

    # Save image
    save_path = os.path.join(OUTPUT_FOLDER, image_name)
    cv2.imwrite(save_path, annotated)

    # Show image
    cv2.imshow("Tomato Disease Detection", annotated)

    print("=" * 60)
    print(f"Image : {image_name}")

    if result.boxes is None or len(result.boxes) == 0:
        print("No disease detected.")
    else:
        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            disease = model.names[class_id]

            print(f"{disease:25s}  {confidence*100:.2f}%")

    print("=" * 60)
    print("Press any key for next image...\n")

    cv2.waitKey(0)

cv2.destroyAllWindows()

print("\nAll images processed successfully.")