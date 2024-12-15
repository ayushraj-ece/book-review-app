from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image
import io
import os
import json

app = Flask(__name__)

API_KEY = 'AIzaSyCV-3Sm90ZZaHCmZ5-rFZeVAlXpcbUt5ck'  # Replace with your valid API key
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Load and process the image
        image = Image.open(file.stream)

        # Example Prompt with Concise Summary and Combined Review
        prompt = (
            "Analyze the uploaded book cover image or ISBN and provide the following details:\n\n"
            "Title: <book_title>\n"
            "Author: <book_author>\n"
            "Genre: <book_genre>\n"
            "Summary: Provide a concise summary of the book in three sections with two-line gaps between them. "
            "The first section should cover the main plot and storyline, "
            "the second should focus on key characters and their roles, "
            "and the third should discuss the themes or key messages the book conveys.\n\n"
            "Review: Provide a brief, balanced review of the book. Mention both positive and negative aspects, "
            "highlighting what readers may enjoy and what might not appeal to everyone.\n\n"
            "If the image is invalid or unrelated to books, respond with: 'Invalid image.'"
        )

        # Send the prompt to the Gemini API
        result = model.generate_content([
            "Image analysis or provided ISBN: ",
            image,  # Include image processing results here (if implemented).
            "\n\n",
            prompt
        ])

        # Extract the generated text
        result_text = result.text.strip()

        # Modify the result text to make subheadings bold and format for better readability
        result_text = result_text.replace("Title:", "<strong>Title:</strong>")
        result_text = result_text.replace("Author:", "<strong>Author:</strong>")
        result_text = result_text.replace("Genre:", "<strong>Genre:</strong>")
        result_text = result_text.replace("Summary:", "<strong>Summary:</strong>")
        result_text = result_text.replace("Review:", "<strong>Review:</strong>")

        return jsonify({'result': result_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
