"""
This endpoint returns all documents
with no hostname created in the last x number
of days

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
import datetime

#Create blueprint
getDocumentsPrinceton_blueprint = Blueprint('getDocumentsPrinceton', __name__)

#Create route
@getDocumentsPrinceton_blueprint.route('/getdocumentsprinceton', methods=['POST'])
@cross_origin(supports_credentials=True)
def getDocumentsPrinceton():
    """This endpoint returns all documents with no hostname created in the last x days"""

    #Grab post data
    data = request.get_json(force=True)

    #grab number of days
    if 'days' not in data:
        return jsonify({'error': 'Days was not provided'})

    #Check for valid Int
    days = data['days']
    isInt = days.isdigit()
    if isInt is False:
        return jsonify({'error': 'Days was not an integer'})

    #Construct date for grabbing data from certain number of days
    today = datetime.datetime.now()
    old_date = today - datetime.timedelta(int(days))

    #Build and execute query
    test_query = {'globalid': {'$exists': 'true'}, "run_date": {'$gte': old_date}}

    #Execute query
    mongo_docs = db.find(test_query)

    #Response dict
    response = {"docs": []}

    #Go through all docs found and append to response
    for doc in mongo_docs:
        #Need to convert objID to string
        copyOfDoc = doc
        copyOfDoc["_id"] = str(doc["_id"])
        response["docs"].append(doc)

    #clean JSON format before returning
    page_sanitized = json.loads(json_util.dumps(response))
    return jsonify(page_sanitized)