import base64
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import os
load_dotenv()

client = OpenAI()

def get_ingredients_from_image(image_path):
    with open(image_path, "rb") as image:
        base64_image = base64.b64encode(image.read()).decode("utf-8")