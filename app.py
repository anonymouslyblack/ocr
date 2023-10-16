from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import pytesseract
import requests

app = Flask(__name__)

# Tesseract OCR API endpoint
OCR_API_URL = "https://api.ocr.space/parse/image"

# Function to extract text from an image using Tesseract OCR API
def extract_text_from_image(image_path, api_key):
    try:
        payload = {
            'apikey': api_key,
        }

        with open(image_path, 'rb') as image_file:
            response = requests.post(OCR_API_URL, files={'image': image_file}, data=payload)
            result = response.json()

            if result.get('OCRExitCode') == 1:
                return result['ParsedResults'][0]['ParsedText'].strip()
            else:
                print(f"Error extracting text from image: {result.get('ErrorMessage', 'Unknown Error')}")
                return ""

    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_images():
    uploaded_images = request.files.getlist('images')
    extracted_texts = []

    for img in uploaded_images:
        if img.filename != '':
            img_path = f"/Users/macintosh/Downloads/{img.filename}"  # Save the uploaded image to a directory
            img.save(img_path)
            text = extract_text_from_image(img_path, 'K85724139088957')  # Replace with your actual API key
            extracted_texts.append(text)

    return render_template('result.html', extracted_texts=extracted_texts)

@app.route('/result')
def result():
    return render_template('result.html', extracted_texts=extracted_texts)


if __name__ == '__main__':
    app.run(debug=True)

