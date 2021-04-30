"""
This endpoint takes in a hostname via POST data
and returns a list of domains run under that
hostname

Author:
Nicholas Prussen
"""

#Import
from flask import Blueprint
from flask import jsonify
from mongo.mongo_client import db
from flask_cors import CORS
from flask_cors import cross_origin
from bson import json_util
import json
from flask import request

#Create blueprint
getDomainsByHostname_blueprint = Blueprint('getDomainsByHostname', __name__)

#Create endpoint
@getDomainsByHostname_blueprint.route("/getdomainsbyhostname", methods = ['POST'])
@cross_origin(supports_credentials=True)
def getDomainsByHostname():
    """
    This endpoint takes a hostname via POST data
    and returns a list of domains found
    """

    #Get POST data
    data = request.get_json(force=True)

    #Grab hostname from data obj
    hostname = data['hostname']

    #Assemble MongoDB query to find domains
    test_query = {'run_information': {'$exists': 'true'},
    'run_information.system_information.hostname': {'$regex': hostname}}

    #Execute query
    mongo_docs = db.find(test_query)

    #structures for returning
    response = {"domains": []}

    #Iterate through docs and grab the domains
    for doc in mongo_docs:

        #Grab domain
        domain = doc['run_information']['run_specifications']['domain']

        #Add to list if not already
        if domain not in response['domains']:
            response['domains'].append(domain)

    #Sanitize JSON and return
    page_sanitized = json.loads(json_util.dumps(response))
    return jsonify(page_sanitized)