import os
import glob
from pathlib import Path
import cv2

from ultralytics import YOLO


BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "data" / "video_sequence"
OUTPUT_VIDEO = BASE_DIR / "outputs" / "vehicle_tracking.mp4"

MODEL_NAME = "yolo11n.pt"

CONFIDENCE = 0.2
FPS = 20

# COCO:
# 2 = car
# 3 = motorcycle
# 5 = bus
# 7 = truck
VEHICLE_CLASSES = [2, 3, 5, 7]


# YOLO modelini yükle
model = YOLO(MODEL_NAME)


# Görüntüleri sırala
image_paths = sorted(
    glob.glob(
        os.path.join(str(IMAGE_DIR), "*.jpg")
    )
)


if len(image_paths) == 0:
    print("Görüntü bulunamadı.")
    exit()


# İlk görüntüyü oku
first_frame = cv2.imread(image_paths[0])

if first_frame is None:
    print("İlk görüntü okunamadı.")
    exit()


# Görüntü boyutları
height, width = first_frame.shape[:2]

print("Width:", width)
print("Height:", height)


# Video oluştur
video_writer = cv2.VideoWriter(
    str(OUTPUT_VIDEO),
    cv2.VideoWriter_fourcc(*"mp4v"),
    FPS,
    (width, height)
)


if not video_writer.isOpened():
    print("VideoWriter açılamadı.")
    exit()


# Frame'leri işle
for i, image_path in enumerate(image_paths):

    frame = cv2.imread(image_path)

    if frame is None:
        print(f"Görüntü okunamadı: {image_path}")
        continue


    # YOLO + ByteTrack
    result = model.track(
        frame,
        persist=True,
        tracker=str(BASE_DIR / "config" / "bytetrack.yaml"),
        classes=VEHICLE_CLASSES,
        conf=CONFIDENCE,
        verbose=False
    )[0]


    boxes = result.boxes


    if boxes is not None and boxes.id is not None:

        xyxy = boxes.xyxy.cpu().numpy()

        class_ids = (
            boxes.cls
            .cpu()
            .numpy()
            .astype(int)
        )

        track_ids = (
            boxes.id
            .cpu()
            .numpy()
            .astype(int)
        )

        confidences = (
            boxes.conf
            .cpu()
            .numpy()
        )


        for box, class_id, track_id, confidence in zip(
            xyxy,
            class_ids,
            track_ids,
            confidences
        ):

            x1, y1, x2, y2 = map(int, box)

            class_name = model.names[class_id]


            # Bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )


            # Araç sınıfı + ID + confidence
            label = (
                f"{class_name} | "
                f"ID:{track_id} | "
                f"{confidence:.2f}"
            )


            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )


    # Frame numarası
    cv2.putText(
        frame,
        f"Frame: {i + 1}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )


    # Videoya yaz
    video_writer.write(frame)

    print(
        f"{i + 1}/{len(image_paths)} işlendi."
    )


video_writer.release()


print("\nAraç takibi tamamlandı.")
print("Video:", OUTPUT_VIDEO)