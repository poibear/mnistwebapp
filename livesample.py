import gradio as gr

from app import app
import numpy as np
from keras.utils import img_to_array
from keras.models import load_model
import cv2

try:
    model_s = load_model("C:\\Users\\JoshL\\Python\\aiwebapps\\numclassify\\app\static\\model\\5Conv1MP_256.h5")
except Exception as e:
    print(f'load your own VALID MNIST model in views.py!!\nerror: {e}')
path = ""
secure_files = []

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    #return whether the file extension is in the given dictionary & has a . in file name
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def evaluate_img(image):
    img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #color to grayscale
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) #otsu to separate pixels to two groups, 
    #greyscale to black/white img
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)) #use smaller input for ai
    dilation = cv2.dilate(thresh, rect_kernel, iterations=5) #define kernel size
    #find connecting images continuous color/brightness change, associate them with a chunk (classification)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #sort contours via classifying their upper left coordinates
    sorted_ctrs = sorted(contours, key=lambda contours: cv2.boundingRect(contours)[0])
    im2 = dilation.copy() #get the final edited image
    results = []
    num_img = 0
    for i in sorted_ctrs: #go through the chunks of contours
        #return coordinates of each corner that enclose the contours
        x, y, w, h = cv2.boundingRect(sorted_ctrs[num_img])
        print(f"x: {x}, y: {y}, w: {w}, h: {h}")
        #get smaller image from orig image
        cropped = im2[y:y+h, x:x+w]
        #define bg into array of one color black
        bg = np.zeros((28, 28), np.uint8)
        if w >= h:
            #resize vs interpolation
            resized = cv2.resize(cropped, (26, int(round(26*h/w))), interpolation=cv2.INTER_AREA)
            rh, rw = resized.shape
            print("shape:", rh, rw)
            bg[round((28-rh)/2):round((28-rh)/2)+rh, 1:27] = resized
        else: #if height greater than width
            resized = cv2.resize(cropped, (int(round(26*w/h)), 26), interpolation=cv2.INTER_AREA)
            rh, rw = resized.shape
            print("shape:", rh, rw)
            bg[1:27, round((28-rw)/2):round((28-rw)/2)+rw] = resized
        #check after results
        # cv2.imshow('resized_centered', bg)
        # cv2.waitKey(0)
        
        x = img_to_array(bg)
        if np.average(x) - 128 > 0:
            x = 255 - x #remove white background outside focus of img
        x /= 255
        x = np.expand_dims(x, axis = 0) #change dimensions so it can perceive grayscale instead of usual color
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