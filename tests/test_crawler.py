import requests
import json
import pytest

test_out_of_pattern = {"status":"bad request. Could not fit pattern"}
error_response = {"status":"bad request. Could not infer tribunal from input"}
expected_response = {}

API = 'http://127.0.0.1:5000'


def test_process_field_not_found_in_request():
    """
    Asserts the response if the 'process_number' field doesn't exists in request json
    """

    wrong_json_file = {
        "processs_numberr":"12345678912345678901"
    }
    
    expected_response = {
        "status":"'process_number' not found in JSON request"
    }

    result = requests.post(API + '/consult', json=wrong_json_file)
    code = result.status_code

    result_dict = json.loads(result.content)
    assert result_dict == expected_response and code == 400


# process doesn't exist
def test_process_does_not_exists():
    """
    Asserts the response if a process was not found at all 
    """

    data = {
        "process_number":"0710802-55.2018.8.02.0000"
    }
    result = requests.post(API + '/consult', json=data)
    code = result.status_code

    assert json.loads(result.content) == test_process_does_not_exists and code == 200

def test_not_enough_data():
    """
    Asserts the response if a process number provided is not sufficient
    """

    json = {
        "process_number":"0710802.2018.8.02.0000"
    }
    result = requests.post(API + '/consult', json=json)
    code = result.status_code

    result_dict = json.loads(result.content)
    assert result_dict == expected_response and code == 200

def test_too_many_digits():
    """
    Asserts the response if a process number provided has too many digits
    """

    json = {
        "process_number":"0710802-55.2018.8.02.00000000"
    }
    result = requests.post(API + '/consult', json=json)
    code = result.status_code

    result_dict = json.loads(result.content)
    assert result_dict == expected_response and code == 200

def test_out_of_pattern():
    """
    Asserts the data fits into expected structure
    """

    data = {
        "process_number":"1s2d3f4g5h6j-55.8.02-0000"
    }
    result = requests.post(API + '/consult', json=data)
    code = result.status_code

    result_dict = json.loads(result.content)
    assert result_dict == test_out_of_pattern and code == 302

def test_could_not_infer_court():
    """
    Asserts the court inference through the pattern. 
    """

    data = {
        "process_number":"0710802-55.2018.8.01.0000"
    }
    result = requests.post(API + '/consult', json=data)
    code = result.status_code

    result_dict = json.loads(result.content)
    assert result_dict == error_response and code == 302


def test_digits_without_hiphen_and_dash():
    """
    Asserts the consult even if the input comes without formatting chars
    """
    
    json = {
        "process_number":"07108025520188020001"
    }
    result = requests.post(API + '/consult', json=json)
    code = result.status_code

    result_dict = json.loads(result.content)
    assert result_dict == expected_response and code == 200

# case: TJAL

# exists on first and second instance
def test_tjal_first_and_second_instance():
    """
    Asserts the response if a process was found in first and second instance
    """
    
    json = {
        "process_number":"0710802-55.2018.8.02.0001"
    }
    result = requests.post(API + '/consult', json=json)
    code = result.status_code

    result_dict = json.loads(result.content)
    assert result_dict == expected_response and code == 200


# exists on first and doesn't in second instance 
def test_tjal_only_in_first_instance():
    """
    Asserts the response if a process was found in first but not in second instance
    """

    data = {
        "process_number":"0021138-09.2011.8.02.0001"
    }
    result = requests.post(API + '/consult', json=data)
    code = result.status_code

    result_dict = json.loads(result.content)
    assert result_dict == expected_response and code == 200



# case: TJCE

# exists on first and second instance
def test_tjce_first_and_second_instance():
    """
    Asserts the response if a process was found in first and second instance
    """
    
    json = {
        "process_number":"0014222-11.2016.8.06.0182"
    }
    result = requests.post(API + '/consult', json=json)
    code = result.status_code

    result_dict = json.loads(result.content)
    assert result_dict == expected_response and code == 200


# exists on first and doesn't in second instance 
def test_tjce_only_in_second_instance():
    """
    Asserts the response if a process was found in second but not in first instance
    """

    json = {
        "process_number":"0000432-74.2023.8.06.0000"
    }
    result = requests.post(API + '/consult', json=json)
    code = result.status_code

    result_dict = json.loads(result.content)
    assert result_dict == expected_response and code == 200

