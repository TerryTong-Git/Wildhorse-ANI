from flask import Flask, send_file
import azure.functions
from flask import request
from .lib.collage.PhotoCollage import collage_maker
from .based import get_from_firebase
from .lib.models.verify import class_n_conf
from .lib.models.score import quality
from .lib.models.find import detection
import os
from io import BytesIO
import json

app = Flask(__name__)

@app.route('/api/HorseFlask/collage', methods = ["POST"])
def collage():

    print(request.json['id'])
    [name,breed]=get_from_firebase(request.json['id'])

    collage_maker('/tmp','/tmp/my_collage.png',1000,1000,1,30,1,name,breed)
    #delete photos after
    #pass request.json id into based
    file_path = '/tmp/output.PNG'
    mimetype = 'image/jpeg'
    return send_file(file_path, mimetype=mimetype)

@app.route('/api/HorseFlask/find', methods = ["POST","GET"])
def findhorse():
    image = BytesIO(request.data)
    return json.dumps(detection(image))

@app.route('/api/HorseFlask/verify', methods=['GET', 'POST'])
def verify():
    #this class takes a binary image and gives a score using our machine learning model. 
    binary_image = BytesIO(request.data)
    classs, conf= class_n_conf(binary_image)
    return json.dumps({"class": classs.replace("\n",""),
            "confidence": float(conf)})

@app.route('/api/HorseFlask/score', methods = ["POST","GET"])
def score():
    binary_image = BytesIO(request.data)
    score = quality(binary_image)
    return json.dumps(float(score))
   
