from ultralytics import YOLO
import cv2
import os

# Load YOLOv8 model
model = YOLO("yolov8n.pt")


# ---------------- IMAGE DETECTION ----------------
def detect_images(image_folder="images"):
    if not os.path.exists(image_folder):
        print(f"Folder '{image_folder}' not found")
        return

    for file in os.listdir(image_folder):
        if file.endswith((".jpg", ".png", ".jpeg")):
            path = os.path.join(image_folder, file)

            img = cv2.imread(path)
            results = model(img)

            for r in results:
                output = r.plot()

            output_path = f"output_{file}"
            cv2.imwrite(output_path, output)
            print(f"Saved: {output_path}")


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

        results = model(frame)

        for r in results:
            output = r.plot()

        cv2.imshow("Vehicle Detection - Video", output)

        # Press ESC to exit
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
        detect_images("images")   # folder name
    elif choice == "2":
        detect_video("test.mp4")
    else:
        print("Invalid choice")