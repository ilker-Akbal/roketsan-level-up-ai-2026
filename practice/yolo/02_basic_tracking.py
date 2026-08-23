from pathlib import Path

from ultralytics import YOLO
import cv2


BASE_DIR = Path(__file__).resolve().parent
model = YOLO("yolo11n.pt")

cap = cv2.VideoCapture(str(BASE_DIR / "data" / "tracking_airplane.mp4"))


while True:
    ret, frame = cap.read()

    if not ret:
        break

    results = model.track(
        frame,
        persist=True,
        classes=[4],
        conf=0.4,
        verbose=False
    )

    result = results[0]

    if result.boxes.id is not None:

        boxes = result.boxes.xyxy.cpu().numpy()
        track_ids = result.boxes.id.int().cpu().tolist()
        confidences = result.boxes.conf.cpu().tolist()

        for box, track_id, confidence in zip(
            boxes,
            track_ids,
            confidences
        ):
            x1, y1, x2, y2 = map(int, box)

            print(
                f"Track ID: {track_id} | "
                f"Confidence: {confidence:.2f} | "
                f"BBox: {x1}, {y1}, {x2}, {y2}"
            )

    annotated_frame = result.plot()

    cv2.imshow("YOLO Tracking", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()