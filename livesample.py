import gradio as gr

import numpy as np
from keras.utils import img_to_array
from keras.models import load_model
import cv2

try:
    model_s = load_model(".\\app\\static\\model\\5Conv1MP_256.h5")
except Exception as e:
    print(f'load your own VALID MNIST model in views.py!!\nerror: {e}')
path = ""
secure_files = []

def evaluate_img(image):
    img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    dilation = cv2.dilate(thresh, rect_kernel, iterations=5)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sorted_ctrs = sorted(contours, key=lambda contours: cv2.boundingRect(contours)[0])
    im2 = dilation.copy()
    results = []
    num_img = 0
    for i in sorted_ctrs:
        x, y, w, h = cv2.boundingRect(sorted_ctrs[num_img])
        print(f"x: {x}, y: {y}, w: {w}, h: {h}")
        cropped = im2[y:y+h, x:x+w]
        bg = np.zeros((28, 28), np.uint8)
        if w >= h:
            resized = cv2.resize(cropped, (26, int(round(26*h/w))), interpolation=cv2.INTER_AREA)
            rh, rw = resized.shape
            print("shape:", rh, rw)
            bg[round((28-rh)/2):round((28-rh)/2)+rh, 1:27] = resized
        else:
            resized = cv2.resize(cropped, (int(round(26*w/h)), 26), interpolation=cv2.INTER_AREA)
            rh, rw = resized.shape
            print("shape:", rh, rw)
            bg[1:27, round((28-rw)/2):round((28-rw)/2)+rw] = resized
        
        x = img_to_array(bg)
        if np.average(x) - 128 > 0:
            x = 255 - x
        x /= 255
        x = np.expand_dims(x, axis = 0) 
        y_proba = model_s.predict(x)
        result = y_proba.tolist()
        pred = int(np.argmax(result, axis=-1))
        results.append([result[0], pred])
        num_img += 1
    results = np.array(results, dtype=object) #dtype to not trigger warning
    problist = results[0][0] #gets the actual list
    predictions = ""
    for index, row in enumerate(problist): #add our probabilties to text
        prediction_prob = np.round(row * 100, 2)
        predictions += f"{index}: {prediction_prob}% \n"
    product = f"""Guessed Number: {results[0][1]}\n{predictions}""" #index as array and not as list
    return [bg, product]

demo = gr.Interface(fn=evaluate_img, inputs="image", outputs=["image", "text"])

demo.launch()