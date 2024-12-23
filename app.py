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
            "Analyze the uploaded book cover image or ISBN and provide the following details in a structured, easy-to-read format with the following subheadings: Title, Author, Genre, Summary, and Review.\n\n"

            "1. **Title:**\n"
            "    - Provide the **full title** of the book. \n"

            "\n2. **Author:**\n"
            "    - Provide the **author's full name**. If the book is written by multiple authors, list them all in the order in which they are credited. If there is an editor or an introduction by someone notable, mention them, but ensure the main author is clearly identified.\n"

            "\n3. **Genre:**\n"
            "    - Identify the **primary genre** of the book. Examples include fiction (literary, historical, science fiction), non-fiction (biography, self-help, memoir), or subgenres like fantasy, mystery, thriller, romance, etc. Be specific, but don’t include niche subgenres unless they are significant to the book’s identity.\n"

            "\n4. **Summary:**\n"
            "    - Provide a **brief summary** of the book. This summary should highlight the key plot elements and the overall story arc. However, **do not reveal major plot twists or resolutions** as it may spoil the reader’s experience.\n"
            "        - **Main Plot and Storyline:** Briefly summarize the **central storyline**. Focus on introducing the setting, the primary conflict, and the direction of the narrative, but avoid spoiling how the plot develops or resolves. Keep the description high-level, without too many specifics on character fates or key twists.\n"
            "        - **Key Characters and Their Roles:** Briefly describe **the protagonist(s)** and **major secondary characters**, focusing on their roles and relationships. Do not give away character arcs or motivations that are central to the plot’s suspense. Mention their general traits and roles in the story, but avoid spoiling their development.\n"
            "        - **Themes and Key Messages:** Identify **the primary themes** of the book without giving away how they unfold in the plot. Themes could include love, justice, betrayal, redemption, or self-discovery. Do not mention how these themes are developed in the plot, keeping this section vague to preserve the suspense.\n"

            "\n5. **Review:**\n"
            "    - **Positive Aspects:** Focus on the **strengths** of the book, highlighting aspects that stand out, such as writing style, character development, the way the suspense is built, the pacing, or how the book keeps the reader engaged. Mention what makes the book exciting or enjoyable without revealing plot details. Emphasize what types of readers might enjoy it, such as fans of suspense, thrillers, or specific genres.\n"
            "        - Be specific about what you liked—describe the **atmosphere**, **writing style**, **character complexity**, or **emotional impact** that makes the book memorable.\n"
            "    - **Negative Aspects:** Offer a balanced view by mentioning **any weaknesses** or areas where the book may not appeal to everyone. This could include **predictability**, **slow pacing**, or sections where the suspense might feel lacking. However, **avoid revealing plot points** that might spoil the experience for readers. Focus on general aspects, such as pacing issues, or if the book might not work for certain reader preferences.\n"
            "        - Be careful not to mention plot details or spoilers. For example, avoid stating whether the protagonist succeeds or fails in their quest.\n"
            "    - **Recommendation:** Suggest **who should read** the book based on the content and themes, like fans of specific genres (e.g., mystery, thriller, fantasy). Explain **why** this book might appeal to them. Then, explain **who might not enjoy** the book, like readers who dislike slow-burn plots or those who don’t enjoy suspenseful stories. This should help potential readers decide if the book is right for them.\n"

            "Please ensure the following formatting guidelines:\n"
            "    - Each section should have a **bold** subheading, followed by the content in clear, readable paragraphs.\n"
            "    - Maintain **appropriate spacing** between sections to ensure the content is well-organized and easy to read.\n"
            "    - Avoid using asterisks, underscores, or any symbols for bold or emphasis. Instead, use **direct bold formatting** in the text.\n"
            "    - Focus on preserving **suspense** by not revealing key plot points, twists, or resolutions. The summary and review should keep the mystery intact for the reader.\n"
            "    - If the image is invalid or unrelated to books, respond with: 'Invalid image.'"
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
    port = os.getenv("PORT", 10000)  # Get port from environment or default to 10000
    app.run(debug=True, host="0.0.0.0", port=int(port))  # Ensure the app binds to the correct port
