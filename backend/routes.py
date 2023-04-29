from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################

# Function to get the picture URL by ID
def get_picture_by_id(id):
    for picture in data:
        if picture['id'] == id:
            return picture
    return None

# Flask route to get picture URL by ID
@app.route('/picture/<int:id>', methods=['GET'])
def get_picture(id):
    picture_data = get_picture_by_id(id)
    if picture_data:
        return jsonify(picture_data)
    else:
        return jsonify({'error': 'Picture not found'}), 404



######################################################################
# CREATE A PICTURE
######################################################################
@app.route('/picture', methods=["POST"])
def create_picture():
    picture_data = request.get_json()
    id = picture_data['id']
    for picture in data:
        if picture["id"] == id:
            return jsonify({"Message": f"picture with id {id} already present"}), 302
    
    data.append(picture_data)    
    return jsonify(picture_data), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route('/picture/<int:id>', methods=['PUT'])
def update_picture(id):
    # Extract picture data from request body
    picture_data = request.get_json()

    picture = get_picture_by_id(id)
    if picture:
        picture.update(picture_data)
        # Return a success response
        return make_response(jsonify({"message": f"picture with id {id} updated successfully"}), 200)
    else:        
        return make_response(jsonify({"message": "picture not found"}), 404)


######################################################################
# DELETE A PICTURE
######################################################################
@app.route('/picture/<int:id>', methods=['DELETE'])
def delete_picture(id):

    picture = get_picture_by_id(id)
    if picture:
        data.remove(picture)
        return make_response(jsonify({"message": f"picture with id {id} removed successfully"}), 204)
    else:        
        return make_response(jsonify({"message": "picture not found"}), 404)


