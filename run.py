import flask;
from flask import request;
from flask import render_template;
from flask import jsonify, make_response;
import os;

import api as api;
from werkzeug.utils import secure_filename;

app = flask.Flask(__name__, template_folder="templates")
app.config["DEBUG"] = True
FOLDER = "./uploads"
app.config['FOLDER'] = FOLDER

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def upFile():
    upfile = request.files['file']
    if request.method=='POST':
        if upfile:
            if request.files:
                name = secure_filename(upfile.filename)
                for existFilename in os.listdir(FOLDER):
                    if(name == existFilename):
                        return "File already exist", 400
                upfile.save(os.path.join(app.config['FOLDER'], name))
                return render_template('home.html')

@app.route('/data.html', methods=['GET'])
def getReport():
    return make_response(jsonify(api.getPayrollReport()), 200)
            
    
    
    

        
app.run()              


        