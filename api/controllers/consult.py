from flask import request, jsonify
from api import app

from api.models.consults import consult_process

@app.route('/consult', methods=['POST'])
def consult():
    process_data = request.get_json()
    if "process_number" in process_data:
        process_number = process_data["process_number"]
        
        response, code = consult_process(process_number)
    else:
        response = {
            "status":"'process_number' not found in JSON request"
        }
        code = 400
    return jsonify(response), code
