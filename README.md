# Parflow Performance Benchmark API
![Generic badge](https://img.shields.io/badge/Flask-yes-green.svg)   

### Description
This API is built using Flask with PyMongo and queries a MongoDB database to serve endpoints to the various React Apps.

## **Quick Start**

### **Requirements:**
- Python virtual environment (VENV/Conda)
   - Install necessary packages
- Store MongoDB connection link (When Developing):
   - ENV Variable

## **Follow these instructions for running while developing**

***Variables to note***
 - [env name]
   - Name of the virtual environment folder than python will create
 - [Mongo Connection Link]
   - Link with valid credentials for MongoDB connection


**1. Open terminal and move to project directory**
 - `$ cd /path/to/parflow-performance-benchmark-flask-api`

**2. Create python virtual environment in root project directory**
 - Using VENV
    - Create a python virtual environment, this will create a folder to contain the environment
        - `$ python3 -m venv [env name]`
    - Activate the virtual environment
        - `$ source [env name]/bin/activate`
    - Install dependencies
        - `$ python3 -m pip install -r requirements.txt`

**3. Store your provided MongoDB connection link**
 - ENV Variable
    - Export variable
        - `$ export MONGO_CONNECTION_LINK="[Mongo Connection Link]"`

**4. Run the Flask API**
 - `$ python3 app.py`

## **Debugging**
To run the API in debugging mode:
 1. Open `app.py` in an editor
 2. Add `debug=True` as a parameter in `app.run([parameters])`

## **Deployment Notes**
 - Deployment on Tuolumne uses Apache with mod_wsgi so using an environment var
for the Mongo Connection Link will not work. Steps for prepping for deployment are below:
   1. Clone the repository onto Tuolumne
   2. Open `mongo/mongo_client.py`
   3. Find the line containing: `connection_string = None`
   4. Replace `None` with your Mongo Connection Link encased in quotations
      - The line should now look like: `connection_string = 'mongodb://...'`
   5. Copy repo files into the mod_wsgi folder, replacing the old deployment files

## **TODO**
- Restructure to use a package like `flask_restful` for authentication and better endpoint management
- Improve endpoint definitons to follow a pattern such as `/adapt/api/documents` or `/princeton/api/documents` to differentiate between requests
  - Restructure file system to also differentiate with subfolders
- POSSIBLE: Use something like `flask_mongoengine` to restrict queries and to automatically escape POST data that may be malicious