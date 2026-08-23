from pathlib import Path

from ultralytics import YOLO
import cv2


BASE_DIR = Path(__file__).resolve().parent
model = YOLO("yolo11n.pt")

cap = cv2.VideoCapture(str(BASE_DIR / "data" / "tracking_test.mp4"))


while True:
    ret, frame = cap.read()

    if not ret:
        break

    results = model(
        frame,
        classes=[0],   # sadece person
        conf=0.4,
        verbose=False
    )

    annotated_frame = results[0].plot()

    cv2.imshow("YOLO Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()