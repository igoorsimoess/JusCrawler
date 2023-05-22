from typing import Tuple


def parse_string(string: any) -> str:
    """
    Grants the number is string formatted
    """
    
    try:
        return str(string)
    except: 
        return "Couldn't cast into string"


def check_number(number: str) -> str:
    """
    Grants the data fits into the pattern by:
        checking digit quantity
        assuming the input can come without separating digits. (then tries to fit into the expected format)
    """
    # transforms on string or exception
    to_be_formatted = parse_string(number)
    
    # if it's received less than the required digits
    if len(to_be_formatted) < 20: 
        return "Not enough data"
    
    # in case just the numbers are received
    elif len(to_be_formatted) == 20:
        try:
            # updates the number to the formatted process.
            number = f"{to_be_formatted[:7]}-{to_be_formatted[7:9]}.{to_be_formatted[9:13]}.{to_be_formatted[13]}.{to_be_formatted[14:16]}.{to_be_formatted[16:]}"
            return number
        except:
            return "Couldn't fit pattern"
    
    # in case the number is already formatted (will be checked for process format in check_tribunal)
    elif len(to_be_formatted) == 25: 
        return number
    else:
        return "Too many digits"
    

def check_tribunal_is_specified(number: str) -> bool:
    '''Checks if in the given string was possible to retrieve the tribunal'''
    if (number[-6]) == '6' or (number[-6] == '2'):
        print(number[-6])
        return True
    else:
        print(number[-6])
        return False 


def return_code(number: str) -> Tuple[dict, int]:

    code = 200
    response = "ok"

    # treats a few bad inputs cases 
    number = check_number(number)
    
    if number == "Not enough data":
        error_response = {"status":"bad request. Not enough data"}
        result, code = error_response, 400 
        return result, code
    
    elif number == "Too many digits":
        error_response = {"status":"bad request. Too many digits"}
        result, code = error_response, 400 
        return result, code
    
    elif number == "Couldn't fit pattern":
        error_response = {"status":"bad request. Could not fit pattern"}
        result, code = error_response, 400 
        return result, code

    if check_tribunal_is_specified(number) == False:
        error_response = {"status":"bad request. Could not infer tribunal from input"}
        result, code = error_response, 400
        return result, code
    else:
        return response, code
