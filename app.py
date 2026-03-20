from ultralytics import YOLO
import cv2

# Load model
model = YOLO("yolov8n.pt")

# Image path
image_path = "test.jpg"

# Read image
img = cv2.imread(image_path)

# Run detection
results = model(img)

# Create output
for r in results:
    output = r.plot()

# Show result
cv2.imshow("Vehicle Detection", output)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save output
cv2.imwrite("output.jpg", output)