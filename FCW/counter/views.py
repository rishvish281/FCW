import requests as requests
from django.shortcuts import render
import tensorflow as tf
from transformers import AutoFeatureExtractor, TFAutoModelForImageClassification
from PIL import Image
import tensorflow as tf
from io import BytesIO
import os
from django.utils.datastructures import MultiValueDictKeyError

print("k\nk\nk\nk\nk\nk\nk\n")
# Load the saved feature extractor and model
saved_extract_path = r"huggingfacemodel"
extractor = AutoFeatureExtractor.from_pretrained(saved_extract_path)
model = TFAutoModelForImageClassification.from_pretrained(saved_extract_path)

# Set the Hugging Face API token
hf_token = "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"
hf_inference_url = f"https://api-inference.huggingface.co/models/eslamxm/vit-base-food101"


def preprocess_image(image_path):
    img = tf.keras.utils.load_img(image_path, target_size=(180, 180))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch of 1 image
    return img_array


# Define a function to make predictions
def predict_image(image_path):
    # Load and preprocess the image
    image = Image.open(image_path)
    inputs = extractor(images=image, return_tensors="tf")

    # Make prediction using the model
    outputs = model(**inputs)
    predictions = tf.nn.softmax(outputs.logits, axis=-1).numpy()

    return predictions


# Create your views here.
def home(request):
    try:
        import requests as rs
        # Assuming your file input field is named 'image_pred'
        uploaded_file = request.FILES['image_pred']

        # Set the path to save the uploaded image in the "uploads" folder
        upload_folder = 'uploads/'
        os.makedirs(upload_folder, exist_ok=True)  # Create the folder if it doesn't exist

        # Set the path to save the uploaded image
        img_path = os.path.join(upload_folder, 'uploaded_image.jpg')

        with open(img_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        image_url = img_path  # Replace with the URL or local path of your image
        response = rs.get(hf_inference_url, headers={"Authorization": f"Bearer {hf_token}"})
        response.raise_for_status()
        predictions = predict_image(image_url)

        import numpy as np
        import re
        # Map the index with the highest probability to the corresponding class label
        predicted_class_index = np.argmax(predictions)
        predicted_class_name = model.config.id2label[predicted_class_index]
        predicted_class_name = str(re.sub('[^a-zA-Z]', ' ', predicted_class_name))
        print(predicted_class_name)



    except MultiValueDictKeyError:
        # Handle the case where 'image_pred' is not present in request.FILES
        uploaded_file = None
        predicted_class_name = None

    import json
    import requests
    if request.method == 'POST':
        # Replace non-letter characters with spaces

        if predicted_class_name is not None:
            query = predicted_class_name
        elif 'query' in request.POST and request.POST['query'].strip():
            query = request.POST['query']
        else:
            query = "default_query"  # Replace with your default query or handle accordingly

        api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
        api_request = requests.get(api_url + query, headers={'X-Api-Key': '38qpCvQ6wfRTy+0eTS4H4Q==E0LFGKc7SgyxSXOB'})

        try:
            api = json.loads(api_request.content)
            print(api_request.content)
        except Exception as e:
            api = "oops! There was an error"
            print(e)
        return render(request, 'home.html', {'api': api})

    else:
        return render(request, 'home.html', {'query': 'Enter a valid query'})
