import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import numpy as np
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions

# Load pre-trained VGG16 model
model = VGG16(weights="imagenet")

# Load and preprocess the image
img_path = "./test_cases/flower.jpg"
img = image.load_img(img_path, color_mode='rgb', target_size=(224, 224))  # VGG16 input size
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

# Predict class probabilities
preds = model.predict(x)

# Decode predictions
decoded_preds = decode_predictions(preds, top=3)[0]  # top 3 predictions
final_preds = []
for i, (imagenet_id, label, prob) in enumerate(decoded_preds):
    final_preds.append(f"{i + 1}: {label} ({prob:.2f})")

for pred in final_preds:
    print(pred)