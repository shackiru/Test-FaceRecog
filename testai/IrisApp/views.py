from django.shortcuts import render, HttpResponse   
from joblib import load
import base64
import io
from .models import Photo
from django.views.decorators.csrf import csrf_exempt
from keras.models import load_model
from time import sleep
from tensorflow.keras.utils import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import threading


model = load('./savedModels/model.joblib')

def predictor(request):
    return render(request, 'main.html')

def index(request):
    return render(request, 'test.html')

def formInfo(request):
    length_1 = request.GET['length_1']
    height_1 = request.GET['height_1']
    length_2 = request.GET['length_2']
    height_2 = request.GET['height_2']
    y_pred = model.predict([[length_1, height_1, length_2, height_2]])
    print(y_pred)
    if y_pred[0] == 0:
        y_pred = 'Setosa'
    elif y_pred[0] == 1:
        y_pred = 'Versicolor'
    else:
        y_pred = 'Virginica'
    return render(request, 'result.html', {'result' : y_pred})

@csrf_exempt
def save_photo(request):
    image_data = request.POST.get('image_data')

    if image_data is None:
        return HttpResponse('Error: No image data provided.')

    # Remove the prefix from the base64 image data
    _, image_base64 = image_data.split(';base64,')

    # Decode the base64 image data
    image_bytes = base64.b64decode(image_base64)

    # Create a new Photo object and save the image
    photo = Photo.objects.create()
    
    # Save the original image
    photo.image.save('snap_photo.png', io.BytesIO(image_bytes))

    # Load the image using OpenCV for face detection
    image_np = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    # Load the pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convert the image to grayscale for face detection
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

    # Perform face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw bounding boxes around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image_np, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Save the modified image with bounding boxes
    _, image_with_boundaries = cv2.imencode('.png', image_np)
    photo.image_with_boundaries.save('snap_photo_with_boundaries.png', io.BytesIO(image_with_boundaries.tobytes()))

    return HttpResponse('OK')