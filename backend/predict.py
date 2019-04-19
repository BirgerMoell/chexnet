import os
from flask import send_file, request, jsonify
from flask import Flask
from flask_cors import CORS
import visualize_prediction as V
import pandas as pd
import warnings
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import base64
import json
import cv2
from io import BytesIO
from PIL import Image


app = Flask(__name__)
CORS(app)
ENCODING = 'utf-8'
# create the folders when setting up your app
os.makedirs(os.path.join(app.instance_path), exist_ok=True)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      #f = request.files['file']
      print("the request is")
      #print(request)
      content = request.json
      #print(content)

      file = content['base64img']
      diagnosis = content['diagnosis']

      starter = file.find(',')
      image_data = file[starter+1:]
      image_data = bytes(image_data, encoding="ascii")
      f = Image.open(BytesIO(base64.b64decode(image_data)))

      # when saving the file
      # This is hardcoded to work with Pneumonia need to fix for all diseases.
      f.save(os.path.join(app.instance_path, secure_filename('00000165_001.png')))
      # prediction
      STARTER_IMAGES=False
      PATH_TO_IMAGES = 'instance'
      PATH_TO_MODEL = "pretrained/checkpoint"
      LABEL="Pneumonia"
      ## Need to figure out how to change the hardcoded values in order to change the diagnosis type
      #LABEL=request.form['diagnosis']
      POSITIVE_FINDINGS_ONLY=True
      # check the data loader for errors
      dataloader,model= V.load_data(PATH_TO_IMAGES,LABEL,PATH_TO_MODEL,POSITIVE_FINDINGS_ONLY,STARTER_IMAGES)
      print("Cases for review:")
      print(len(dataloader))
      # check the show_next for errors
      preds, imglocation=V.show_next(dataloader,model, LABEL)
      print(preds)
      print(imglocation)
      encodedimage = ""

      # img = cv2.imread(imglocation)
      # _, img_encoded = cv2.imencode('.jpg', img)

      # Encode image
      with open(imglocation, "rb") as image_file:
         encodedimage = base64.b64encode(image_file.read())
      # Encoded image
      #print(encodedimage)
      # Base 64 string from image
      base64_string = encodedimage.decode(ENCODING)
      jsonfiles = json.loads(preds.to_json())
      return jsonify({ 'prediction': jsonfiles, 'encodedimage': base64_string  })