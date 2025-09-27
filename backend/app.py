from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

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
        if uploaded_file.filename != '':
            print("Arquivo recebido!")

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