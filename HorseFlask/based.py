import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import requests
import os

# Use a service account.
def get_from_firebase(id):
    # print(id)
    # cred = credentials.Certificate('./HorseFlask/hourse-hd-firebase-adminsdk-v7fns-5ed4f7e8b6.json')

    # app = firebase_admin.initialize_app(cred, {
    #     'storageBucket': 'hourse-hd.appspot.com'
    # })

    db = firestore.client()

    ref  = db.collection('horses')
    dic = ref.document(f"{id}").get().to_dict()
    
    download_file(dic["sideImage"],  '/tmp/sideImage.jpg')
    download_file(dic["frontImage"],  '/tmp/frontImage.jpg')
    download_file(dic["faceImage"], '/tmp/faceImage.jpg' )
    # download_file(dic["sideImage"],  './HorseFlask/misc/sideImage.jpg')
    # download_file(dic["frontImage"],  './HorseFlask/misc/frontImage.jpg')
    # download_file(dic["faceImage"], './HorseFlask/misc/faceImage.jpg' )

    return [dic['name'], dic['breed']]

def download_file(url, destination):
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Check if the request was successful

    with open(destination, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:  # Filter out keep-alive chunks
                file.write(chunk)

# get_from_firebase("2CeXeqvhKItaJoXwJRnf")







