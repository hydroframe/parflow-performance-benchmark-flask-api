"""
This is the endpoint for returning a list of documents based
on hostname and domain passed by POST

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

#Create blueprint
getDocumentsByHostnameDomain_blueprint = Blueprint('getDocumentsByHostnameDomain', __name__)

#Create endpoint
@getDocumentsByHostnameDomain_blueprint.route("/getdocumentsbyhostnamedomain", methods = ['POST'])
@cross_origin(supports_credentials=True)
def getDocumentsByHostnameDomain():
    """This endpoint returns a list of docs found with
    a specific hostname and domain sent bv POST.

    Please note, hostname is referred to as "runname" throughout

    TODO Break this def into multiple helper defs
    """

    #Grab POST data
    data = request.get_json(force=True)

    #Grab POST data vars
    hostname = data['docParams']['hostname']
    runname = data['docParams']['runname']

    #Assemble query and execute
    test_query = {'run_information': {'$exists': 'true'},
    'run_information.system_information.hostname': {'$regex': hostname},
    'run_information.run_specifications.domain': runname}
    docs = db.find(test_query)

    #Empty arrays for holding core counts and dicts
    run_core_counts = []
    query_results_doc_holder = []

    #Get all processor topologies
    for doc in docs:
        #Store each doc
        query_results_doc_holder.append(doc)
        #Tear apart topology and get core count
        topology_string = doc['run_information']['run_specifications']['processor_topology']
        topology_array = topology_string.split(" ")
        current_doc_total_cores = 1
        for number in topology_array:
            current_doc_total_cores = (current_doc_total_cores * int(number))
        if current_doc_total_cores not in run_core_counts:
            run_core_counts.append(current_doc_total_cores)
    
    #seperated docs by core count
    runDocsSeperated = {}

    #make dictionary labels for core counts
    for number in run_core_counts:
        runDocsSeperated[number] = {}

    #iterate through all docs and append into runDocsSeperated
    for doc in query_results_doc_holder:
        
        #get topology again
        topology_string = doc['run_information']['run_specifications']['processor_topology']
        topology_array = topology_string.split(" ")
        current_doc_total_cores = 1
        for number in topology_array:
            current_doc_total_cores = (current_doc_total_cores * int(number))

        #get id for assigning a unique name
        docID = str(doc['_id'])

        #sort into dicts
        runDocsSeperated[current_doc_total_cores][docID] = doc

    #sanitize the page and return
    page_sanitized = json.loads(json_util.dumps(runDocsSeperated))
    return jsonify(page_sanitized)