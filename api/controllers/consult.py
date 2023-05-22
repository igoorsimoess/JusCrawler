from flask import request, jsonify
from api import app

from api.models.consults import consult_process
from api.helpers.helpers import return_code


# builds the consult route/endpoint
@app.route('/consult', methods=['POST'])
def consult():
    """
    triggers the crawler and scraper consult_process method
    treats the request body
    treats the response content
    """
    process_data = request.get_json()

    # following clean code parameters, treats errors before success case
    if "process_number" not in process_data:
        response = {
            "status":"'process_number' not found in JSON request"
        }
        code = 400
        return response, code
    
    else:
        process_number = process_data["process_number"]

        # treat request 
        response, code = return_code(process_number)

        if code == 400:
            return response, code

        # if passed through filters, perform scrape
        else:
            response, code = consult_process(process_number)

            return jsonify(response), code
    