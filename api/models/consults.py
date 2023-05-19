from multiprocessing import Queue, Process

from crawler.jus_crawler.spiders.spider_jus import search_justice
from crawler.jus_crawler.spiders.spider_jus_2 import search_justice_second_instance


def parse_string(string: any):
    """
    Grants the number is string formatted
    """
    
    try:
        return str(string)
    except: 
        return "Couldn't cast into string"


def check_number(number: str):
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
    

def check_tribunal_is_specified(number: str):
    '''Checks if in the given string was possible to retrieve the tribunal'''
    if (number[-6]) == '6' or (number[-6] == '2'):
        print(number[-6])
        return True
    else:
        print(number[-6])
        return False 

def consult_process(number: str) -> dict:
    """
    Builds the process in order to run two consults in parallel
    """

    code = 200

    process_details_first_instance = Queue()
    process_details_second_instance = Queue()

    # treats some a few bad inputs cases 
    number = check_number(number)
    
    if check_tribunal_is_specified(number) == False:
        error_response = {"status":"bad request. Could not infer tribunal from input"}
        result, code = error_response, 302 
        return result, code
    
    if number == "Not enough data":
        error_response = {"status":"bad request. Not enough data"}
        result, code = error_response, 302 
        return result, code
    
    elif number == "Too many digits":
        error_response = {"status":"bad request. Too many digits"}
        result, code = error_response, 302 
        return result, code
    
    elif number == "Couldn't fit pattern":
        error_response = {"status":"bad request. Could not fit pattern"}
        result, code = error_response, 302 
        return result, code    



    process1 = Process(target=search_justice, args=(number, process_details_first_instance ))
    process2 = Process(target=search_justice_second_instance, args=(number, process_details_second_instance))

    process1.start()
    process2.start()

    process1.join()
    process2.join()


    result = {
        "Primeira Instancia": process_details_first_instance.get(),
        "Segunda Instancia": process_details_second_instance.get(),
    }

    return result, code

