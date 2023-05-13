import os
from flask import render_template, request, flash
from app import app
from app.forms import (UploadForm, ResultForm)
from datetime import datetime
from werkzeug.utils import secure_filename
import numpy as np
from keras.utils import img_to_array
#from keras.preprocessing import image
from keras.models import load_model
from PIL import Image
import cv2

try:
    ROOT_DIR = os.path.realpath(os.path.join(os.path.join(os.path.dirname(__file__), '.\\static\\model\\')))
    model_s = load_model(os.path.join(ROOT_DIR, '5Conv1MP_256.h5'))
    #model_s = load_model(os.path.join(os.path.dirname(__file__), "static/model/5Conv1MP_256.h5"))
    #load_model(os.path.join(os.path.dirname(__file__), "static/model/5Conv1MP_256.h5"))
except Exception as e:
    print(f'load your own MNIST model in views.py!!\nerror: {e}')
path = ""
secure_files = []

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    #return whether the file extension is in the given dictionary & has a . in file name
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def evaluate_img(path):
    img = cv2.imread(path) #use cv2 type
    #cv2.imshow('threh', img) #show it original
    #cv2.waitKey(0) #close popup lul, no waitkey means we dont wait for window to close
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('threh', gray) #show it gray
    #cv2.waitKey(0)
    #color to grayscale
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) #otsu to separate pixels to two groups, 
    #greyscale to black/white img
    #cv2.imshow("threh", thresh)
    #cv2.waitKey(0)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)) #use smaller input for ai
    dilation = cv2.dilate(thresh, rect_kernel, iterations=5) #define kernel size
    #find connecting images continuous color/brightness change, associate them with a chunk (classification)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #sort contours via classifying their upper left coordinates
    sorted_ctrs = sorted(contours, key=lambda contours: cv2.boundingRect(contours)[0])
    im2 = dilation.copy() #get the final edited image
    results = []
    num_img = 0
    try:
        x = os.mkdir(path[:-4])
    except:
        print('mkdir error', x)
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
        #store cropped img to our image folder before predictions
        char_path = os.path.join(path[:-4], str(num_img) + ".png")
        print(char_path)
        cv2.imwrite(char_path, bg)
        #img_path = char_path.split("app")[1] #what does this even do???
        img_path = char_path.strip("/")
        img_path = img_path.replace("\\", "/") #everything to forward slash
        
        x = img_to_array(bg)
        if np.average(x) - 128 > 0:
            x = 255 - x #remove white background outside focus of img
        x /= 255
        x = np.expand_dims(x, axis = 0) #change dimensions so it can perceive grayscale instead of usual color
        y_proba = model_s.predict(x)
        result = y_proba.tolist()
        pred = int(np.argmax(result, axis=-1))
        results.append([result[0], pred, img_path])
        num_img += 1
    return (results)

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if request.method == 'POST' and form.validate_on_submit(): #if you uploaded & validated ok
        file = form.file.data
        if file and allowed_file(file.filename): #if valid extension
            filename = secure_filename(file.filename) #checks if filename has alphanumeric symbols (e.g., instead of SQL) & converts to ASCII
            new_filename = str(datetime.timestamp(datetime.now())) + \
                os.path.splitext(filename)[1] #add some uniqueness
            path = os.path.join(app.root_path,
                                'static/img/upload', new_filename)
            #os.path.join('static/img/upload', new_filename)
            file.save(path)
            results = evaluate_img(path)
            # result = evaluate_img(path, form.white_background.data)
            #pred = int(np.argmax(results, axis = -1))
            form = ResultForm()
            return render_template("result.html", title="Results", form = form,
                                   path = os.path.join('static/img/upload', new_filename),
                                   results = results)
        else:
            msg = "wrong file format: " + file.filename
            flash(msg, "warning")
            return render_template('index.html', title="Home", form = form)
    else:
        return render_template('index.html', title="Home", form = form)

@app.route('/about', methods=['GET'])
@app.route('/about.html', methods=['GET'])
def about():
    return render_template("about.html", title="About")
