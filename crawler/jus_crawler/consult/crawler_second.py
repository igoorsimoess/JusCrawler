from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import re


class Crawler_2_Instance():
    def __init__(self, number: str):
        # complete number
        self.number = self.check_number(number)
        # the tribunal url
        self.tribunal = self.check_tribunal(self.number)
        # foro number
        self.foro = self.get_foro(self.number)
        # first 13 digits
        self.unified_number = self.get_unified_number(self.number)

    # def successfull_found(self, string: str):
    #     presence_of_unique_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2[class='subtitle']")))
    #     if presence_of_unique_element:
    #         return True
    #     else:
    #         return False


    def parse_string(self, string: any):
        """
        Grants the number is string formatted
        """
        
        try:
            return str(string)
        except: 
            return "Couldn't cast into string"

            
    def get_unified_number(self, number):
        """
        Returns the first 13 digits of number
        """
        pattern = r'^(\d+-\d+\.\d+\.)'

        match = re.match(pattern, number)
        if match:
            unified_number = match.group(1)
            return unified_number 


    def get_foro(self, number):
        '''
        Retrieves the "foro" attribute from the process number (last 4 digits)
        '''
        
        foro = number[-4:]
        return foro 
    

    def check_number(self, number: str):
        """
        Grants the data fits into the pattern by:
            checking digit quantity
            assuming the input can come without separating digits. (then tries to fit into the expected format)
        """
        # transforms on string or exception
        to_be_formatted = self.parse_string(number)
        
        # if it's received less than the required digits
        if len(to_be_formatted) < 20: 
            return "Not enough data"
        
        # in case just the numbers are received
        elif len(to_be_formatted) == 20:
            try:
                # updates the number to the formatted process.
                return f"{to_be_formatted[:7]}-{to_be_formatted[7:9]}.{to_be_formatted[9:13]}.{to_be_formatted[13]}.{to_be_formatted[14:16]}.{to_be_formatted[16:]}"
            except:
                return "Couldn't fit pattern"
        
        # in case the number is already formatted (will be checked for process format in check_tribunal)
        elif len(to_be_formatted) == 25: 
            return number
        else:
            return "Too many digits"

    def check_tribunal(self, number: str):
        """
        Checks the tribunal based on digit pattern
        Defines the court URL (AL or CE)
        """
        self.check_number(number)

        pattern = r'^\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$'
        match = re.match(pattern, self.number)
    
        if match:
            number_in_15th_position = self.number[19]
                
            if number_in_15th_position == '2':
                return 'https://www2.tjal.jus.br/cposg5/open.do' 
            
            elif number_in_15th_position == '6':
                return 'https://esaj.tjce.jus.br/cposg5/open.do'
        
            else:
                return 'Court yet to come'
        
        else:
            return 'Pattern did not match'

    def consult(self):
        modal_select_process = False
        presence_of_unique_element = False
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(options=chrome_options)

            wait = WebDriverWait(driver, 10)

            driver.get(self.tribunal)
            process_number = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='numeroDigitoAnoUnificado']")))
            process_number.send_keys(self.unified_number)

            process_number = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='foroNumeroUnificado']")))
            process_number.send_keys(self.foro)

            submit_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit']")))
            submit_button.click()
            try:
                modal_select_process = driver.find_element(By.CSS_SELECTOR, "article[class='modal__lista-processos']")
                if modal_select_process:
                    select_input = driver.find_element(By.CSS_SELECTOR, "input[name='processoSelecionado']")
                    select_input.click()
                    submit = driver.find_element(By.CSS_SELECTOR, "input[name='btEnviarIncidente']")
                    submit.click()
            except:
                print('CHEGOU NA Exception')
                pass

            response_url = driver.current_url

            # checks if is in the process detail page (intended)
            try:
                presence_of_unique_element = driver.find_element(By.CSS_SELECTOR, "tbody[id='tabelaUltimasMovimentacoes']")
            except:
                pass
            if presence_of_unique_element:
                print(' TRUE TRUE TRUE TRUE----------------------------- ENTROU')
                driver.quit()
                return response_url
            else:
                driver.quit()
                print('AQUI ----------------------------- ENTROU')
                return "Couldn't find the process"
             
        except Exception as e:
            print(e)
