from flask import Flask, render_template, request
import torch
import numpy as np
import cv2
from gradcam import GradCAM

# Load the trained model
model = torch.load('model3_080423.pth')

app = Flask(__name__)

# Define a route to serve the HTML form
@app.route('/')
def index():
    return render_template('BoneMaturityLab.html')

# Define a route to handle the form submission
@app.route('/', methods=['POST'])
def predict():
    # Get the user input from the form
    gender = int(request.form['male'])
    age = int(request.form['boneage'])
    
    # Make a prediction using the model
    input_data = np.array([[gender, age]])
    predicted_age = model.predict(input_data)[0][0]

    # Render the prediction result in an HTML page
    return render_template('result.html', predicted_age=predicted_age)

@app.route('/gradcam', methods=['POST'])
def gradcam():
    # receive the image from the request
    img = request.files['image'].read()

    # convert the image to a NumPy array
    npimg = np.fromstring(img, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # initialize the GradCAM model
    model = torch.load('model3_080423.pth')  # load your model here
    gradcam = GradCAM(model=model, layer=model.conv5)

    # generate the GradCAM visualization
    heatmap = gradcam.generate_heatmap(img)

    # convert the heatmap to an image and return it as a response
    heatmap_img = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    response = cv2.imencode('.png', heatmap_img)[1].tostring()

    return response, 200, {'Content-Type': 'image/png'}

if __name__ == '__main__':
    app.run()