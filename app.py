from ultralytics import YOLO
import cv2
import os

# Load YOLO model
model = YOLO("yolov8n.pt")

# Vehicle classes (COCO)
VEHICLE_CLASSES = [2, 3, 5, 7]  # car, bike, bus, truck


# ---------------- IMAGE DETECTION ----------------
def detect_images(folder="images"):
    if not os.path.exists(folder):
        print(f"Folder '{folder}' not found")
        return

    for file in os.listdir(folder):
        if file.endswith((".jpg", ".png", ".jpeg")):
            path = os.path.join(folder, file)

            img = cv2.imread(path)
            results = model(img, conf=0.5)

            vehicle_count = 0

            for r in results:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    if cls in VEHICLE_CLASSES:
                        vehicle_count += 1

                output = r.plot()

            output_path = f"output_{file}"
            cv2.imwrite(output_path, output)

            print(f"{file} → Vehicles detected: {vehicle_count}")

            with open("log.txt", "a") as f:
                f.write(f"{file} → {vehicle_count} vehicles\n")


# ---------------- VIDEO DETECTION ----------------
def detect_video(video_path="test.mp4"):
    if not os.path.exists(video_path):
        print("Video file not found")
        return

    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, conf=0.5)

        vehicle_count = 0

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                if cls in VEHICLE_CLASSES:
                    vehicle_count += 1

            output = r.plot()

        # Overlay count
        cv2.putText(output, f"Vehicles: {vehicle_count}",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2)

        cv2.imshow("Vehicle Detection", output)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


# ---------------- MAIN ----------------
if __name__ == "__main__":
    print("1 → Image Detection")
    print("2 → Video Detection")

    choice = input("Enter choice: ")

    if choice == "1":
        detect_images("images")
    elif choice == "2":
        detect_video("test.mp4")
    else:
        print("Invalid choice")