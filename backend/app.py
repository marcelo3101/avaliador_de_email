# Lib imports
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pypdf import PdfReader

import chardet

# Local Imports
from utils.files import *

# Configuring static folder to serve the frontend files
app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app)

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/verify_email", methods=["POST"])
def verify_email():
    msg = ""

    if request.files:
        msg = "File included"
        uploaded_file = request.files['file']  # 'file' is the name of the input field that receives the file in the frontend portion.
        # uploaded_file.stream.read()
        print(uploaded_file.filename)
        if check_file_extension(uploaded_file.filename):
            print("Arquivo válido recebido!")
            
            # Handling the file types
            if (uploaded_file.mimetype == "text/plain" or uploaded_file.mimetype == "message/rfc822"):  # Text files
                print("text file")
                # Read all contents
                raw_content = uploaded_file.stream.read()
                encoding = chardet.detect(raw_content)["encoding"]
                print(f"Encoding {encoding}")
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

        return jsonify({
            "response": msg,
            "status": 200,
            "file_text_text": text
        }), 200

    elif request.form:
        msg = "Form included"

    else:
        msg = "No files or form included"

    # Response dict
    response = {
        "response": msg,
        "status": 200  # Default successful status code
    }

    # Return JSON response and respective status code
    return jsonify(response), response["status"]