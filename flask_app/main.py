from flask import Flask, request, jsonify, render_template
from brick_model_summarizer.main import process_brick_file
import io

app = Flask(__name__)

# Limit file upload size to 16 MB
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB


@app.route("/")
def upload_page():
    """Serve the HTML upload page."""
    return render_template("upload.html")


@app.route("/api/process-ttl", methods=["POST"])
def process_ttl_file():
    """Process the uploaded TTL file and return JSON data."""
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Backend validation for file extension
    if not file.filename.lower().endswith(".ttl"):
        return jsonify({"error": "Only .ttl files are allowed"}), 400

    try:
        # Read the uploaded file into memory
        file_content = file.stream.read()

        # Create a temporary in-memory file for processing
        in_memory_file = io.BytesIO(file_content)
        in_memory_file.name = file.filename  # Simulate file name for Brick processing

        # Process the in-memory file with the BRICK summarizer
        building_data = process_brick_file(in_memory_file)

        return jsonify(building_data), 200

    except Exception as e:
        return jsonify({"error": f"Failed to process file: {str(e)}"}), 500


if __name__ == "__main__":
    app.run()
