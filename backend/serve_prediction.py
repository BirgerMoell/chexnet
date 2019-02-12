import visualize_prediction as V
import pandas as pd
import warnings
from flask import send_file, request
from flask import Flask
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    print(request.files)
    file = request.files['file']
    file.filename="our.jpg"
    print(file.filename)
    file.save(file.filename)
    testimage = scipy.misc.imresize(scipy.misc.imread(file),(150,150))
    print(testimage.shape)
    testimage = testimage.reshape((1,) + testimage.shape)
    prediction = loaded_model.predict(testimage).astype(float)
    print(prediction)
    return jsonify({ 'classification': { 'cat': prediction[0][0], 'dog' : 1-prediction[0][0]} })

@app.route('/diagnose', methods=['POST'])
def getPrediction():
    return 'Hello, World!'


#suppress pytorch warnings about source code changes
warnings.filterwarnings('ignore')

STARTER_IMAGES=True
PATH_TO_IMAGES = "starter_images/"

#STARTER_IMAGES=False
#PATH_TO_IMAGES = "your path to NIH data here"

PATH_TO_MODEL = "pretrained/checkpoint"
LABEL="Pneumonia"
POSITIVE_FINDINGS_ONLY=True

dataloader,model= V.load_data(PATH_TO_IMAGES,LABEL,PATH_TO_MODEL,POSITIVE_FINDINGS_ONLY,STARTER_IMAGES)
print("Cases for review:")
print(len(dataloader))

preds=V.show_next(dataloader,model, LABEL)
preds

if __name__ == '__main__':
    app.run(debug=True)

