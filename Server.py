from flask import Flask, request, render_template,url_for,redirect, flash, make_response
import torch
import numpy as np
import pickle
import os
import urllib.request
import uuid
from fileinput import filename
from posixpath import splitext
from PIL import Image
import sys
from unittest import result
import os


app = Flask(__name__)
WEB_APP=os.path.dirname(os.path.abspath(__file__))
UPLOADFOLDER = 'static/IMAGEUPLOADS/'
WAB_APP=os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = "cairocoders-ednalan"
app.secret_key = "secret key"
app.config['UPLOADFOLDER'] = UPLOADFOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define a route to serve the HTML form
@app.route('/')
def index():
    return render_template("BoneMaturityLab.html")

@app.route('/, methods=["GET","POST"]')
def BoneMaturityLab():
    file = request.files['image']
    if file.filename =='':
        flash('No Image Selected For Uploading')
        return redirect(request.url)
    target=os.path.join(WEB_APP, 'static/IMAGEUPLOADS/')
    if not os.path.isdir(target):
      os.mkdir(target)
    upload=request.files.getlist("file")[0]
    print("File name: {}".format(upload.filename))
    filename=str(uuid.uuid1())+upload.filename
    ext=os.path,splitext(upload.filename)[1]
    if (ext==".jpg") or (ext==".png") or (ext==".dcm") or (ext==".JPG") or (ext==".jpeg") or (ext==".JPEG") or (ext==".PNG"):
      print("File accepted")
    destination = os.path.join(filename + target)
    print("File saved to:", destination)
    upload.save(destination)
    img =  filename #target
    # Get the image file from the user
    model = torch.load('model3_080423.py')
    img = []
    img = request.files['image_predict'].read()
    img = Image.open(img)
    # Preprocess the image
    img = img.resize((256,256))
    img.append(img)
    img = np.array(img)
    img = np.expand_dims(img,axis=0)
    # Make a Prediction
    pred = model.predict(img)
    boneage = pred[0][0]
    print(f'img = {boneage}')
    if request.method == "POST":
    # getting input with name = lname in HTML form 
      resp=make_response(render_template("result.html", name = f"{filename}",boneage = boneage,filename=filename))
      resp.set_cookie("file", filename)
      return resp

@app.route('/result')
def result():
    filename = '4360.png'
    gender = 'Male' if True else 'Female'
    pred = 108
    return render_template("result.html", filename =filename,gender = gender,boneage = pred)

@app.route('/display/<filename>')
def showimage(filename):
   return redirect(url_for('static', filename='IMAGEUPLOADS/'+ filename),code = 301)

if __name__ == '__main__':
    app.run(debug=True)