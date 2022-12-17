# MNIST Web App
## Overview
Uses an MNIST model for number classification, displaying the model's results on a webpage.

## Requirements
- ~~Python >= 3.11.x~~
- Python <= 3.10.x
- Flask
- Flask-WTF
- keras
- Keras-Preprocessing
- numpy
- Pillow
- waitress
- WTForms
- Tensorflow

#### tested versions
- Flask==2.2.2
- Flask-WTF==1.0.1
- keras==2.11.0
- Keras-Preprocessing==1.1.2
- numpy==1.23.5
- Pillow==9.3.0
- waitress==2.1.2
- WTForms==3.0.1

### note
packages can be downloaded from the `requirements.txt` file

## Usage
Run the `run.py` file. Waitress/Flask will open a localhost port (as specified) for the webpage to be accessed.