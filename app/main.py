from flask import Flask, request
from database_manager import DatabaseManager
from screenshot_processor import ScreenshotProcessor
from search_engine import SearchEngine
from storage_manager import StorageManager
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Initialize database manager and search engine
db_manager = DatabaseManager()
search_engine = SearchEngine()

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    os.getenv("USERNAME"): generate_password_hash(os.getenv("PASSWORD"))
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route('/upload', methods=['POST'])
@auth.login_required
def upload():
    try:
        file = request.files['image']
        if file:
            # Create the 'tmp' directory if it doesn't exist
            os.makedirs('tmp', exist_ok=True)

            # Define a unique file name and save the file temporarily
            image_path = os.path.join('tmp', secure_filename(file.filename))
            file.save(image_path)
            
            # Process and store the image
            screenshot_processor = ScreenshotProcessor(db_manager, search_engine)
            screenshot_processor.process_and_store(image_path)

            return {'message': 'Image processed and stored.'}, 200
        else:
            return {'error': 'No image file in request.'}, 400
    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/search', methods=['GET'])
@auth.login_required
def search():
    search_query = request.args.get('q')
    search_engine = SearchEngine()
    results = search_engine.search_images(search_query)
    return {'results': results}, 200

@app.route('/delete/<image_id>', methods=['DELETE'])
@auth.login_required
def delete(image_id):
    try:
        db_manager = DatabaseManager()
        db_manager.delete_image(image_id)
        storage_manager = StorageManager()
        storage_manager.delete(image_id)
        search_engine = SearchEngine()
        search_engine.delete_image(image_id)
        return {'message': 'Image and related data have been deleted.'}, 200
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
