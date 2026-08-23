# Day 02 — Computer Vision, YOLO and Tracking

This folder covers three small computer-vision exercises:

- `preprocessing.py` — resize, crop, RGB/gray conversion, normalization and Gaussian blur.
- `classification.py` — transfer learning with MobileNetV2.
- `detection_tracking.py` — YOLO detection plus ByteTrack multi-object tracking on a JPG frame sequence.

## Data

- `data/sample.jpg` is used by the preprocessing example.
- Put classification data under `data/Dataset/<class_name>/...`.
- Put tracking frames under `data/video_sequence/`.

Large videos, generated outputs and model weights are ignored by Git.
