"""
This is the endpoint for returning an individual document based
off objID

Author:
Nicholas Prussen
"""

#Imports
from flask import Blueprint
from flask import jsonify
from mongo.mongo_client import db
from flask_cors import CORS
from flask_cors import cross_origin
from bson import json_util
import json
from flask import request
from bson.objectid import ObjectId

#Assign blueprint
getDocumentByID_blueprint = Blueprint('getDocumentByID', __name__)

#Create Endpoint
@getDocumentByID_blueprint.route("/getdocumentbyid", methods = ['POST'])
@cross_origin(supports_credentials=True)
def getDocumentByID():
    """ This endpoint takes an ObjID, validates it and returns the info
    linked to that ID
    """
    #Grab data doc from POST
    data = request.get_json(force=True)

    #Validate objID, return bad doc if not good
    if ObjectId.is_valid(data['docID']) is not True:
        return jsonify({'valid': "false"})

    #Query doc from db and execute
    test_query = {'_id': ObjectId(data['docID'])}
    doc = db.find_one(test_query)

    #Make sure doc exists
    if doc is not None:
        #Convert date to nice format
        converted_date = doc['run_date'].isoformat()
        doc['run_date'] = converted_date
    else:
        #Catch none found
        doc = {'valid': "false"}

    #sanitize and return
    page_sanitized = json.loads(json_util.dumps(doc))
    return jsonify(page_sanitized)