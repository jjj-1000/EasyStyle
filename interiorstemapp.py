from flask import Flask, render_template, request, jsonify, redirect, url_for
import os

import requests
from io import BytesIO
from PIL import Image
from datetime import datetime

current_dir = os.getcwd()

template_dir = os.path.join(current_dir, 'templates')
app = Flask(__name__, template_folder=template_dir)



if not os.path.exists('static'):
    os.makedirs('static')
    print("Created 'static' directory.")

@app.route('/')
def home():
    return render_template('frontlook.html')

@app.route('/speakpage.html')
def speakpage():
    return render_template('speakpage.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/result')
def result_page():
    image_url = request.args.get('image_url')
    if not image_url:
        return redirect(url_for('home'))
    return render_template('result.html', image_url=image_url)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        text_input = request.form.get('text_input')
        if not text_input:
            return jsonify({'status': 'error', 'message': 'No text input provided'}), 400

        prompt = text_input
        print(f"Generating image for prompt: '{prompt}'")
        url = f"https://image.pollinations.ai/prompt/{prompt}"

        response = requests.get(url)

        image = Image.open(BytesIO(response.content))
        print("Image generated.")
        filename = f"generated_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        image_path = os.path.join('static', filename)
        image.save(image_path)
        print(f"Image saved to {image_path}")
        return jsonify({'status': 'success', 'image_url': f'/static/{filename}'})

    except Exception as e:
        print(f"Error during image generation: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
