import base64
import json
import sys
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import os
load_dotenv()

client = OpenAI()

def get_ingredients_from_image(image_path):
    with open(image_path, "rb") as image:
        base64_image = base64.b64encode(image.read()).decode("utf-8")
         
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system", "content": """ You are a chef and a user needs your help to make a dish. 
                They send you an image of the ingredients they have and you give them a recipe based on the ingredients.
                Use the following JSON format:

{
    "reasoning": "reasoning for the total calories",
    "ingredients list": [
        {
            "name": " name of the ingredient",
            "calories": "calories in the ingredient"
        }
    ],
    "total": "total calories in the meal"
}"""
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": " Give me a recipe based on the ingredients in the image."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            },
        ],
    )

    response_message = response.choices[0].message
    content = response_message.content

    return json.loads(content)

if __name__ == "__main__":
    image_path = sys.argv[1]
    calories = get_ingredients_from_image(image_path)
    print(json.dumps(calories, indent=4))