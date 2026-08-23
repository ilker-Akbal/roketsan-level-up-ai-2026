from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np


BASE_DIR = Path(__file__).resolve().parent
image_path = BASE_DIR / "data" / "sample.jpg"
output_dir = BASE_DIR / "outputs"
output_dir.mkdir(parents=True, exist_ok=True)

# Görüntüyü oku
image = cv2.imread(str(image_path))

if image is None:
    print("Image bulunamadı")
    exit()


# Orijinal görüntüyü göster
cv2.imshow("Original Image", image)

cv2.waitKey(0)
cv2.destroyAllWindows()


# Görüntü boyutları
height, width, channels = image.shape

print(f"Height: {height}")
print(f"Width: {width}")
print(f"Channels: {channels}")


# Resize
resized_image = cv2.resize(
    image,
    (640, 360)
)

resized_height, resized_width = resized_image.shape[:2]

print(f"Resized Height: {resized_height}")
print(f"Resized Width: {resized_width}")


# Crop sınırlarını belirle
x1 = int(resized_width * 0.2)
x2 = int(resized_width * 0.8)

y1 = int(resized_height * 0.2)
y2 = int(resized_height * 0.8)


# Crop
cropped_image = resized_image[y1:y2, x1:x2]

cv2.imshow("Cropped Image", cropped_image)

cv2.waitKey(0)
cv2.destroyAllWindows()


# BGR -> RGB
rgb_image = cv2.cvtColor(
    resized_image,
    cv2.COLOR_BGR2RGB
)

plt.imshow(rgb_image)
plt.title("RGB Image")
plt.axis("off")
plt.show()


# Grayscale
gray_image = cv2.cvtColor(
    resized_image,
    cv2.COLOR_BGR2GRAY
)

plt.imshow(
    gray_image,
    cmap="gray"
)

plt.title("Gray Image")
plt.axis("off")
plt.show()


# Normalization
normalized_image = resized_image.astype(np.float32) / 255.0

print("Normalized Min:", normalized_image.min())
print("Normalized Max:", normalized_image.max())


# Gaussian Blur
blurred_image = cv2.GaussianBlur(
    resized_image,
    (15, 15),
    0
)

cv2.imshow("Blurred Image", blurred_image)

cv2.waitKey(0)
cv2.destroyAllWindows()


cv2.imwrite(str(output_dir / "resized.jpg"), resized_image)