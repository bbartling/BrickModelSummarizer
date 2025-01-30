from flask import Flask, request, jsonify, render_template, session
from brick_model_summarizer.main import (
    load_graph_once,
    get_class_tag_summary,
    get_ahu_information,
    get_zone_information,
    get_building_information,
    get_meter_information,
    get_central_plant_information,
    get_vav_boxes_per_ahu,
)
import io
import time
import uuid

app = Flask(__name__)
app.secret_key = "super_secret_key"  # Used for Flask session security

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Store user-specific graphs in memory (not global)
user_graphs = {}

AVAILABLE_COMPONENTS = {
    "class_tag_summary": get_class_tag_summary,
    "ahu_information": get_ahu_information,
    "zone_information": get_zone_information,
    "building_information": get_building_information,
    "meter_information": get_meter_information,
    "central_plant_information": get_central_plant_information,
    "number_of_vav_boxes_per_ahu": get_vav_boxes_per_ahu,
}

@app.route('/')
def upload_page():
    """Serve the HTML upload page."""
    # Assign a unique session ID if one doesn't exist
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())  # Generate a unique ID for the user
    return render_template('upload.html')

@app.route('/api/upload-ttl', methods=['POST'])
def upload_ttl_file():
    """Upload and process the TTL file, storing it per user."""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Session error. Please refresh the page."}), 400

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.lower().endswith('.ttl'):
        return jsonify({"error": "Only .ttl files are allowed"}), 400

    try:
        # Read file into memory
        file_content = file.stream.read()
        in_memory_file = io.BytesIO(file_content)
        in_memory_file.name = file.filename

        # Load graph and store it per user
        user_graphs[user_id] = load_graph_once(in_memory_file)

        return jsonify({"message": "File uploaded and processed successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to process file: {str(e)}"}), 500

@app.route('/api/get-component', methods=['GET'])
def get_component():
    """Retrieve a specific component from the user's cached graph."""
    user_id = session.get("user_id")

    if not user_id or user_id not in user_graphs:
        return jsonify({"error": "No TTL file uploaded. Please upload a file first."}), 400

    requested_component = request.args.get('component')

    if requested_component in AVAILABLE_COMPONENTS:
        return jsonify({requested_component: AVAILABLE_COMPONENTS[requested_component](user_graphs[user_id])}), 200
    return jsonify({"error": "Invalid component requested"}), 400

if __name__ == '__main__':
    app.run()
