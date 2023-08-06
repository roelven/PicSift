from flask import Flask, request, jsonify, g
from werkzeug.security import check_password_hash
from screenshot_processor import ScreenshotProcessor
from database_manager import DatabaseManager
from search_manager import SearchManager
from flask_httpauth import HTTPBasicAuth
from dotenv import load_dotenv
import os

app = Flask(__name__)
auth = HTTPBasicAuth()
load_dotenv()

screenshot_processor = ScreenshotProcessor()
database_manager = DatabaseManager()
search_manager = SearchManager()

@auth.verify_password
def verify_password(username, password):
    if username == 'admin' and check_password_hash(os.getenv('USER_ADMIN'), password):
        return username

@app.route('/upload', methods=['POST'])
@auth.login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'message': 'File type not supported'}), 400

    image_path = os.path.join('/tmp/', file.filename)
    
    try:
        file.save(image_path)
    except Exception as e:
        return jsonify({'message': f'File could not be saved. Error: {str(e)}'}), 500

    image_url, text = screenshot_processor.process_screenshot(image_path)
    metadata = database_manager.insert_image_data(file.filename, image_url, text)
    search_manager.index_document(metadata)

    return jsonify({'message': 'File uploaded and processed', 'data': metadata}), 201

@app.route('/delete/<string:image_id>', methods=['DELETE'])
@auth.login_required
def delete_image(image_id):
    try:
        metadata = database_manager.get_image_data(image_id)
        if metadata is None:
            return jsonify({'message': 'No image found with the provided ID'}), 404

        database_manager.delete_image_data(image_id)
        search_manager.delete_document(image_id)
        screenshot_processor.storage_manager.delete(metadata['image_url'])

        return jsonify({'message': 'Image deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Could not delete image. Error: {str(e)}'}), 500

@app.route('/search', methods=['GET'])
@auth.login_required
def search():
    search_term = request.args.get('q', None)
    if not search_term:
        return jsonify({'message': 'Search term not provided'}), 400

    results = search_manager.search_documents(search_term)
    return jsonify({'message': 'Search results', 'data': results}), 200

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
