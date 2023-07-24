import pytest
import json
import re

#do not have an init file
from HorseFlask.flaskapp import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def image_file():
    return open('tests/images/Moving.jpg', 'rb')
    

def test_score(client, image_file):
        
        response = client.post('/api/HorseFlask/score', data=image_file)
        response_string = response.data.decode()
        res_data = json.loads(response_string)

        assert response.status_code == 200
        assert isinstance(res_data, float)

def test_verify(client, image_file):
     
        response = client.post('/api/HorseFlask/verify', data=image_file)
        resp_string = response.data
        resp = json.loads(resp_string)
        class_data = resp['class']
        conf_data = resp['confidence']

        assert response.status_code == 200
        assert isinstance(class_data, str)
        assert isinstance(conf_data, float)
        assert class_data == 'Body' or class_data == 'Profile' or class_data == 'Front'

def is_base64_image(image_data):
    # Regular expression pattern for base64 encoded data
    base64_pattern = r'^([A-Za-z0-9+/=]+\s*)*$'

    # Check if the image_data matches the base64 pattern
    return re.match(base64_pattern, image_data) is not None
            

def test_find(client,image_file):
        
        response = client.post('/api/HorseFlask/find', data=image_file)
        resp_string = response.data
        resp = json.loads(resp_string)
        horse_data = resp['horses']
        other_data = resp['others']

        for i in horse_data:
            image = i[0]
            confidence = i[1]
            assert is_base64_image(image) is True
            assert type(confidence) == float
        
        for i in other_data:
            image = i[0]
            confidence = i[1]
            assert is_base64_image(image) is True
            assert type(confidence) == float

        assert response.status_code == 200
        
        
      




     