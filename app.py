import base64
import json
import sys
from flask import Flask, request, jsonify, render_template
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set up OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_ingredients_from_image(image_path):
    with open(image_path, "rb") as image:
        base64_image = base64.b64encode(image.read()).decode("utf-8")

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system", 
                "content": """You are a chef and a user needs your help to make a dish. 
                They send you an image of the ingredients they have and you give them a recipe based on the ingredients.
                Use the following JSON format:

{
    "reasoning": "reasoning for the total calories",
    "ingredients list": [
        {
            "name": "name of the ingredient",
            "calories": "calories in the ingredient"
        }
    ],
    "total": "total calories in the meal"
}"""
            },
            {
                "role": "user",
                "content": "Give me a recipe based on the ingredients in the image."
            },
            {
                "role": "user",
                "content": f"data:image/jpeg;base64,{base64_image}"
            },
        ],
    )

    response_message = response['choices'][0]['message']['content']
    return json.loads(response_message)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        # Save the uploaded image to a temporary location
        file_path = os.path.join('static', 'uploads', file.filename)
        file.save(file_path)

        # Process the image to get ingredients and calories
        ingredients_info = get_ingredients_from_image(file_path)
        return jsonify(ingredients_info)

if __name__ == '__main__':
    os.makedirs(os.path.join('static', 'uploads'), exist_ok=True)
    app.run(debug=True)
