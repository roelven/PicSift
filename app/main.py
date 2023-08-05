from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash

from screenshot_processor import ScreenshotProcessor
from search_engine import SearchEngine
from database_manager import DatabaseManager

app = Flask(__name__)
auth = HTTPBasicAuth()

# initialize processor, database manager and search engine
screenshot_processor = ScreenshotProcessor()
database_manager = DatabaseManager()
search_engine = SearchEngine()

@auth.verify_password
def verify_password(username, password):
    stored_password = os.getenv(f'USER_{username.upper()}')
    if not stored_password:
        return False
    return check_password_hash(stored_password, password)

@app.route('/upload', methods=['POST'])
@auth.login_required
def upload_screenshot():
    # handle screenshot upload
    pass

@app.route('/search', methods=['GET'])
@auth.login_required
def search_screenshots():
    # handle screenshot search
    pass

@app.route('/delete', methods=['POST'])
@auth.login_required
def delete_screenshot():
    # handle screenshot deletion
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
