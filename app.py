from flask import Flask, request, render_template
from model import ImageClassifier
from PIL import Image
import numpy as np
import os

app = Flask(__name__)
classifier = ImageClassifier()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    img_path = os.path.join('static/uploads', file.filename)
    file.save(img_path)
    
    img = Image.open(img_path)
    img_array = np.array(img)
    predictions = classifier.classify_image(img_array)
    
    return render_template('index.html', predictions=predictions)

if __name__ == '__main__':
    app.run(debug=True)
