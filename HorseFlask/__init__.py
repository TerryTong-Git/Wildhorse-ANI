import azure.functions as func
from .flaskapp import app
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('./HorseFlask/hourse-hd-firebase-adminsdk-v7fns-5ed4f7e8b6.json')

apps = firebase_admin.initialize_app(cred, {
        'storageBucket': 'hourse-hd.appspot.com'
    })
def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)