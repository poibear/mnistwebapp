import os
from flask import render_template, request, flash
from app import app
from app.forms import (UploadForm, ResultForm)
from datetime import datetime
from werkzeug.utils import secure_filename
import numpy as np
from keras.utils import load_img, img_to_array
from keras.models import load_model

model_s = load_model(os.path.join(os.path.dirname(__file__), "static/model/mnist.h5"))
path = ""
secure_files = []

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    #return whether the file extension is in the given dictionary & has a . in file name
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#actual ai stuff
def evaluate_img(path):
    img = load_img(path, color_mode = 'grayscale', target_size = (28, 28))
    # # Inverting the image.
    # if white_bg:
    #     img = Image.fromarray(np.invert(img))
    x = img_to_array(img)
    if np.average(x) - 128 > 0:
        x = 255 - x #remove white background outside focus of img
    x /= 255
    x = np.expand_dims(x, axis = 0)
    y_proba = model_s.predict(x)
    result = y_proba.tolist()
    return (result)

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
            result = evaluate_img(path)
            # result = evaluate_img(path, form.white_background.data)
            pred = int(np.argmax(result, axis = -1))
            form = ResultForm()
            return render_template("result.html", title="Results", form = form,
                                   path = os.path.join('static/img/upload', new_filename),
                                   result = result[0], pred = pred)
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
