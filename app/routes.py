from flask import request, jsonify, abort
from services import create_screenshot, process_screenshot, ProcessingError
from ocr import process_image
from database import update_screenshot, save_screenshot, get_screenshots, get_screenshot, DatabaseError
from storage import upload_image, delete_image

@app.route('/screenshots', methods=['POST'])
def upload_screenshot():
    # Extract the file from the request
    file = request.files.get('screenshot')
    if not file:
        return jsonify(error="No file provided"), 400

    # Extract metadata, if provided
    metadata = request.form.get('metadata', '{}')

    try:
        # Process the screenshot and upload it to cloud storage
        screenshot_data = process_screenshot(file)

        # Merge the received metadata and the new data
        screenshot_data.update(json.loads(metadata))

        # Save the data to the database
        screenshot_id = save_screenshot(screenshot_data)

    except (ProcessingError, DatabaseError) as e:
        # Return a 500 error and the error message
        return jsonify(error=str(e)), 500

    # Return a response with the screenshot ID
    return jsonify(id=screenshot_id), 202

@app.route('/screenshots', methods=['GET'])
def list_screenshots():
    # Fetch the page number and size from the query parameters, or use defaults
    page = request.args.get('page', default=1, type=int)
    size = request.args.get('size', default=50, type=int)

    try:
        # Fetch the list of screenshots from the database
        screenshots = get_screenshots(page=page, size=size)
    except DatabaseError as e:
        # Return a 500 error and the error message
        return jsonify(error=str(e)), 500

    # Return the list of screenshots
    return jsonify(screenshots=screenshots)


@app.route('/screenshots/<id>', methods=['GET'])
def get_screenshot(id):
    try:
        # Fetch the screenshot from the database
        screenshot = get_screenshot(id)
    except DatabaseError as e:
        # Return a 500 error and the error message
        return jsonify(error=str(e)), 500
    
    if screenshot is None:
        # If the screenshot doesn't exist, return a 404 error
        abort(404)

    # Return the screenshot
    return jsonify(screenshot=screenshot)


@app.route('/screenshots', methods=['POST'])
def post_screenshot():
    # Extract the file from the request
    file = request.files['file']

    try:
        # Process the image with the OCR engine
        text = process_image(file)

        # Upload the image to the cloud storage
        url = upload_image(file)

        # Create a new screenshot in the database
        screenshot = create_screenshot(file.filename, text, url)
    except (DatabaseError, OCRProcessingError, ImageUploadError) as e:
        # Return a 500 error and the error message
        return jsonify(error=str(e)), 500

        # remove file after processing (check with ChatGPT)
        os.remove(file.path)

    # Return the created screenshot
    return jsonify(screenshot=screenshot), 201


@app.route('/screenshots/<id>', methods=['PUT'])
def update_screenshot(id):
    # Get the updated metadata from the request
    metadata = request.json

    try:
        # Update the screenshot in the database
        screenshot = update_screenshot(id, metadata)

        if screenshot is None:
            # If no screenshot was found with the given ID, return a 404 error
            return jsonify(error='Not Found'), 404
    except DatabaseError as e:
        # If there was a database error, return a 500 error
        return jsonify(error=str(e)), 500

    # Return the updated screenshot
    return jsonify(screenshot=screenshot)


@app.route('/screenshots/<id>', methods=['DELETE'])
def delete_screenshot(id):
    try:
        # Get the screenshot from the database
        screenshot = get_screenshot(id)

        if screenshot is None:
            # If no screenshot was found with the given ID, return a 404 error
            return jsonify(error='Not Found'), 404

        # Delete the image from the cloud storage
        delete_image(screenshot['url'])

        # Delete the screenshot from the database
        delete_screenshot(id)
    except (DatabaseError, ImageDeleteError) as e:
        # If there was a database error or an error deleting the image, return a 500 error
        return jsonify(error=str(e)), 500

    # Return a success message
    return jsonify(message='Screenshot deleted')