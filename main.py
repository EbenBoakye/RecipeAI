from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import os
load_dotenv()

client = OpenAI()