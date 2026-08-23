from pathlib import Path

import numpy as np
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


# Ayarlar
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "Dataset"

IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 10


# -----------------------------
# Dataset
# -----------------------------

train_ds = keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="training",
    seed=42,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

val_ds = keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)


class_names = train_ds.class_names

print("Sınıflar:", class_names)


# Veri yüklemeyi hızlandır
train_ds = train_ds.prefetch(tf.data.AUTOTUNE)
val_ds = val_ds.prefetch(tf.data.AUTOTUNE)


# -----------------------------
# Data Augmentation
# -----------------------------

data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.05),
    layers.RandomZoom(0.1)
])


# -----------------------------
# MobileNetV2
# -----------------------------

base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)


# MobileNet ağırlıklarını dondur
base_model.trainable = False


# -----------------------------
# Model
# -----------------------------

inputs = keras.Input(shape=(224, 224, 3))

x = data_augmentation(inputs)

x = preprocess_input(x)

# HATA BURADAYDI
x = base_model(x, training=False)

x = layers.GlobalAveragePooling2D()(x)

x = layers.Dropout(0.2)(x)

outputs = layers.Dense(
    len(class_names),
    activation="softmax"
)(x)


model = keras.Model(
    inputs=inputs,
    outputs=outputs
)


# -----------------------------
# Compile
# -----------------------------

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


model.summary()


# -----------------------------
# Train
# -----------------------------

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS
)