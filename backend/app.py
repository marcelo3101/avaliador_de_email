# Lib imports
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pypdf import PdfReader

import chardet

# Local Imports
from backend.utils.files import *
from backend.utils.models import classify_and_generate_response, generate_response_from_template

# Configuring static folder to serve the frontend files
app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app)

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/verify_email", methods=["POST"])
def verify_email():
    if request.files:
        uploaded_file = request.files['file']  # 'file' is the name of the input field that receives the file in the frontend portion.

        if check_file_extension(uploaded_file.filename):
            # Handling the file types
            if (uploaded_file.mimetype == "text/plain" or uploaded_file.mimetype == "message/rfc822"):  # Text files
                # Read all contents
                raw_content = uploaded_file.stream.read()
                encoding = chardet.detect(raw_content)["encoding"]
                text = raw_content.decode(encoding)
            
            elif (uploaded_file.mimetype == "application/pdf"):
                print("PDF file")
                reader = PdfReader(uploaded_file)
                text = ""
                for page_number in range(len(reader.pages)):
                    page = reader.pages[page_number]
                    text += page.extract_text()

        else:
            return jsonify({
                "error": "Invalid file extension"
            }), 400

    elif request.form:
        text = request.form.get("text")

    else:
        return jsonify({
            "error": "No data provided",
            "status": 400
        }), 400
    
    # Classify received text and generate response for it
    response = classify_and_generate_response(text).split("&&", 1)
    classification = response[0]
    response_suggestion = response[1]
    bool_classification = True if classification == "Produtivo" else False
    template_response_suggestion = generate_response_from_template(bool_classification, text)

    # Return classification and suggested response
    return jsonify({
        "classification": classification,
        "response_suggestion": response_suggestion,
        "template_suggestion": template_response_suggestion,
        "status": 200
    }), 200