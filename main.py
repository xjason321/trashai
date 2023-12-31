from PIL import Image
import tensorflow as tf
import numpy as np
import os
import sklearn
from sklearn.preprocessing import LabelEncoder

def pre_process(path):
    image = Image.open(path)
    width, height = image.size

    pixels = list(image.getdata())
    pixels = [pixels[i : i + width] for i in range(0, len(pixels), width)]

    return pixels
    
x_train = []
y_train = []

x_test = []
y_test = []

for folder in ['battery', 'biological', 'brown-glass', 'cardboard', 'clothes', 'green-glass', 'metal', 'paper', 'plastic', 'shoes', 'trash', 'white-glass']:
        num_files = len(os.listdir(f"train_data/{folder}"))

        print(f"Folder {folder} has {num_files} images.")
        for file in os.listdir(f'train_data/{folder}'):
            path = f'train_data/{folder}/{file}'

            x_train.append(pre_process(path))
            
            y_train.append(folder)
            
print('checkpoint #1')

x_train = np.array(x_train)
# x_test = np.array(x_test)

x_train = x_train.reshape(-1, 255, 255, 3)  # Reshape x_train to match input shape
# x_test = x_test.reshape(-1,255,255, 3)
print("checkpoint #2")

label_encoder = LabelEncoder()
y_train = label_encoder.fit_transform(y_train)
# y_test = label_encoder.fit_transform(y_test)

print("checkpoint #3")

x_train = x_train / 255.0  # Normalize pixel values

print("checkpoint #4")

model = tf.keras.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=(255, 255, 3)))
model.add(tf.keras.layers.Dense(200, activation="relu"))
model.add(tf.keras.layers.Dense(200, activation="relu"))
model.add(tf.keras.layers.Dense(200, activation="relu"))
model.add(tf.keras.layers.Dense(200, activation="relu"))
model.add(tf.keras.layers.Dense(12, activation="softmax"))

print("checkpoint #5")

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

print('part2 dog-eater')

model.fit(x_train, y_train, epochs=20)

print('hey')


model.save('trash.model')

print('done')