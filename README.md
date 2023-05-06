# MNIST Web App
## Overview
Uses an MNIST model for number classification, displaying the model's results on a webpage.

## Requirements
- Python >= 3.11.x
- Flask
- Flask-WTF
- keras
- numpy
- waitress
- WTForms
- Tensorflow

#### tested versions
- Tensorflow==2.11.1
- Flask==2.3.2
- Flask-WTF==1.1.1
- keras==2.11.0
- numpy==1.24.1
- waitress==2.1.2
- WTForms==3.0.1

### note
packages can be downloaded from the `requirements.txt` file
```
pip install -r requirements.txt
```

## Usage
Run the `run.py` file. Waitress/Flask will open a localhost port (as specified) for the webpage to be accessed.
You will need to supply this webapp with your own MNIST model. A guide can be found on Tensorflow