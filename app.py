"""
This file imports all API endpoints and runs the main Flask App

Authors:
Nicholas Prussen
"""

#Imports
from flask import Flask
from flask_cors import CORS
from flask_cors import cross_origin

#Import db connection from mongo_client
from mongo.mongo_client import db

#Import API Endpoints
from api.getHostnames import getHostnames_blueprint
from api.getDomainsByHostname import getDomainsByHostname_blueprint
from api.getDocumentsByHostnameDomain import getDocumentsByHostnameDomain_blueprint
from api.getDocumentByID import getDocumentByID_blueprint
from api.getDocumentsPrinceton import getDocumentsPrinceton_blueprint

#Configure Flask App
app = Flask(__name__)
CORS(app, support_credentials=True)

#Register blueprints
app.register_blueprint(getHostnames_blueprint)
app.register_blueprint(getDomainsByHostname_blueprint)
app.register_blueprint(getDocumentsByHostnameDomain_blueprint)
app.register_blueprint(getDocumentByID_blueprint)
app.register_blueprint(getDocumentsPrinceton_blueprint)

#Root connection, can be used as a simple check to see if API is working
@app.route("/")
@cross_origin(supports_credentials=True)
def root():
    return "You aren't supposed to be here :)"

#Run the flask app
if __name__ == "__main__":
    app.run(threaded=True, host=('0.0.0.0'))
