import requests
import json

API = 'http://127.0.0.1:5000'


def test_process_field_not_found_in_request():
    """
    Asserts the response if the 'process_number' field doesn't exists in request json
    """

    wrong_json_file = {
        "processs_numberr":"12345678901234567890"
    }

    result = requests.post(API + '/consult', json=wrong_json_file)

    assert result.status_code == 400


# process doesn't exist
def test_process_does_not_exists():
    """
    Asserts the response if a process was not found at all 
    """

    data = {
        "process_number":"0710802-55.2018.8.02.0000"
    }
    
    result = requests.post(API + '/consult', json=data)

    not_found = ({'Primeira Instancia':[{'data': 'Process not found'}],'Segunda Instancia':[{'data': 'Process not found'}]})
    result_dict = json.loads(result.content)
    assert result_dict == not_found and result.status_code == 200

def test_not_enough_data():
    """
    Asserts the response if a process number provided is not sufficient
    """

    data = {
        "process_number":"0710802.2018.8.02"
    }
    result = requests.post(API + '/consult', json=data)
    code = result.status_code

    expected_response = {"status":"bad request. Not enough data"}

    result_dict = json.loads(result.content)
    assert result_dict == expected_response and code == 400

def test_too_many_digits():
    """
    Asserts the response if a process number provided has too many digits
    """

    data = {
        "process_number":"0710802-55.2018.8.02.00000000"
    }
    result = requests.post(API + '/consult', json=data)

    expected_response = {"status":"bad request. Too many digits"}
    result_dict = json.loads(result.content)

    assert result_dict == expected_response and result.status_code == 400


def test_could_not_infer_court():
    """
    Asserts the court inference through the pattern. 
    """

    data = {
        "process_number":"0710802-55.2018.8.01.0000"
    }

    result = requests.post(API + '/consult', json=data)
    
    expected_response = {"status":"bad request. Could not infer tribunal from input"}

    result_dict = json.loads(result.content)

    assert result_dict == expected_response and result.status_code == 400


def test_digits_without_hiphen_and_dash():
    """
    Asserts the consult even if the input comes without formatting chars
    """
    
    data = {
        "process_number":"07108025520188020001"
    }
    result = requests.post(API + '/consult', json=data)
    code = result.status_code

    assert code == 200

# case: TJAL

def test_consult_tjal():
    """
    Asserts successfull GET request to API using TJAL parameters
    """

    data = {
        "process_number":"0021138-09.2011.8.02.0001"
    }
    result = requests.post(API + '/consult', json=data)
    code = result.status_code

    assert code == 200



# case: TJCE

def test_consult_tjce():
    """
    Asserts successfull GET request to API using TJCE parameters 
    """
    
    data = {
        "process_number":"0014222-11.2016.8.06.0182"
    }
    result = requests.post(API + '/consult', json=data)
    code = result.status_code

    assert code == 200



