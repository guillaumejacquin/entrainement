
from flask import Flask
from flask import render_template, url_for, request
import sys
from main import *
from flask_cors import CORS
from flask import jsonify
from main import *
import os
sys.path.append("../")
from app import *
app = Flask(__name__)
CORS(app)
from werkzeug.utils import secure_filename


import json

uploads_dir = os.path.join(app.instance_path, '')


@app.route("/add", methods=["POST"])
def transform_files_to_json():
    csv = request.files['csv']
    json2 = request.form.get('json')
    json_object = json.loads(json2)

    csv.save(os.path.join('', csv.filename))


    with open("smart-contracts-data.json", 'w') as f:
        json.dump(json_object, f)

    try:
        data_to_json = DataToJson()
        data_to_json.transform_json_and_csv_to_json()

        return jsonify(1)
    except Exception:
        return jsonify(0)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
