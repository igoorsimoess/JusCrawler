#JusCrawler

## The Project

This project intends to improve the experience of retrieving public data from process details



### How to run the project:

##### clone the repository
``` 
git clone <this repository>
```
##### Create a virtual environment

```
pip install virtualenv
virtualenv juscrawler
```

##### install all dependecies

```
pip install -r requirements.txt
```

##### Run the API

``` 
python run.py
```
##### Perform a consult:

Open any client service and perform a request to localhost on port 5000.

```
127.0.0.1:5000/consult

# JSON format expected:

"process_number":"0000000-00.0000.0.02.0000"
"process_number":"0000000-00.0000.0.06.0000"
```
### Some Tools in this project:
- Scrapy
- Selenium
- Flask
- Pytest

#### Some cool features
- In order to enhance the crawler perfomance, multiprocessing was applied in API call in order to run two spiders in parallel    
This enhanced the time for scraping the data by 2. The meantime for consulting is between 6 - 7 seconds to retrieve the data

- Some input checks was made: 
    - The API infers the Court (Tribunal de Justiça de Alagoas ou do Ceará) by the input pattern.
    - The API considers:
        - Too many digits in input
        - Number out of format
        - bad formatting of JSON request 
- Some webpages can get pretty tricky to base the script logic, hence, in order to bypass this problem a combination of scrapy and selenium was used to crawl and scrape the 4 web pages in this project (2 court instances for each)

- Regex was vastly used since some CSS could be in many sorts of formats

#### Some features in progress

The project consults a public database of process details. In order to assert the tests for API, a file with mock data would be necessary.
However, a better approach would be to use *jsonschema* to compare the expected data based on type. This approach is, in addition to better structured,
more suited to the type of data. Hence, this function is being implemented in the future to have automated tests without the need for a large mock file with public data.