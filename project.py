from flask import Flask, render_template, request
from keras.models import load_model
import numpy as np
from keras.preprocessing import image
import geocoder
from datetime import datetime
import pandas as pd
import joblib
import os
import subprocess
import webbrowser 

html_file_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
webbrowser.open(html_file_path)

g = geocoder.ip('me')
address = g.address

month_text = datetime.now().strftime("%B")

class_names = {2: "Clayey Soil", 1: "Black Soil", 3: "Red Soil", 0: "Alluvial Soil"}

soil_model = load_model(filepath="soil_model.h5")

model3 = joblib.load('crop_recommendation_model.joblib')

if month_text in ["June", "July", "August", "September", "October"]:
    Mtype = 5
    Mname = "Kharif"
elif month_text in ["November", "December", "January", "February", "March", "April", "May"]:
    Mtype = 4
    Mname = "Rabi"

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('project.html')

@app.route('/process_data', methods=['POST'])
def process_data():
    # Get the uploaded file from the form
    uploaded_file = request.files['s_image']
    # Save the uploaded file to a specific location
    upload_folder = 'uploaded_images'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    uploaded_file.save(os.path.join(upload_folder, uploaded_file.filename))

    # Get other form data
    rainfall = request.form['Rainfall']

    # Process the uploaded image
    image_path = os.path.join(upload_folder, uploaded_file.filename)
    new_img = image.load_img(image_path, target_size=(244, 244))
    img = image.img_to_array(new_img)
    img = np.expand_dims(img, axis=0)
    prediction = soil_model.predict(img)
    prediction = np.argmax(prediction, axis=1)

    Stype = 0  # Default value
    if class_names[prediction[0]] == "Clayey Soil":
        Stype = 2
    elif class_names[prediction[0]] == "Black Soil":
        Stype = 1
    elif class_names[prediction[0]] == "Red Soil":
        Stype = 3

    new_data = pd.DataFrame({'Type of Soil': [Stype], 'Season': [Mtype], 'Rainfall in mm': [rainfall]})
    prediction3 = model3.predict(new_data)

    result_message = f"<h3>Your Soil Type is {class_names[prediction[0]]}<br><br>address : {address}<br><br>season : {Mname}</h3><br><br><h2>Best Grown Crop in your field: {prediction3[0]}</h2>"

    return result_message


if __name__ == '__main__':
    # Start the Flask server in a separate process
    flask_process = subprocess.Popen(['python', 'budget.py'])
    app.run(debug=True)
