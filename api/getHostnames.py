"""
This endpoint returns all hostnames in the database
to fill a dropdown menu

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

#Create blueprint
getHostnames_blueprint = Blueprint('getHostnames', __name__)

#Create route
@getHostnames_blueprint.route('/gethostnames')
@cross_origin(supports_credentials=True)
def getHostnames():
    """This endpoint takes in no data and returns a list of hostnames"""

    #Build and execute MongoDB query
    test_query = {'run_information': {'$exists': 'true'},
    'run_information.system_information.hostname': {'$exists': 'true'}}
    #Projection to only grab run_information
    project_query = {'run_information': 1}

    #Execute query
    mongo_docs = db.find(test_query, projection=project_query)

    #Create dict with an array that will hold all unique hostnames found
    response = {"hostnames": []}

    #Loop through found documents and grab hostnames
    for doc in mongo_docs:

        #Grab hostname
        doc_hostname = doc['run_information']['system_information']['hostname']

        #Check if already exists
        if doc_hostname not in response['hostnames']:
            response['hostnames'].append(doc_hostname)

    #clean JSON format before returning
    page_sanitized = json.loads(json_util.dumps(response))
    return jsonify(page_sanitized)