
# JusCrawler

## The Project

This projects intends to improve the access for the public data by providing, developing and integrating an API + Crawler which retrieves public data from processes details of TJAL Tribunal de Justiça de Alagoas and TJCE Tribunal de Justiça do Ceará.


### How to run the project:

##### clone the repository
``` 
git clone <this repository>
```
##### Create and activate your virtual environment

```
pip install virtualenv
virtualenv juscrawler
. juscrawler/bin/activate
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

Open any client service like Insomnia or Postman and perform a request to localhost on port 5000 using the /consult endpoint and sending the following JSON structure: 

```
127.0.0.1:5000/consult

# JSON format expected:

"process_number":"0000000-00.0000.0.02.0000"
"process_number":"0000000-00.0000.0.06.0000"
```
or simply:
```
00000000000000020000 -> 20 chars
```
### Some Tools in this project:
- Scrapy
- Selenium
- Flask
- Pytest

#### Some cool features
- In order to enhance the crawler perfomance, multiprocessing was applied in API call in order to run two spiders in parallel.    
This enhanced the scraping time by 2. The average time for consulting is now between 6 - 7 seconds. 

- Some input checks was made: 
    - The API infers the Court (Tribunal de Justiça de Alagoas ou do Ceará) by the input pattern.
    - The API considers:
        - Too many digits in input
        - Number out of format
        - bad formatting of JSON request 
- Some webpages can get pretty tricky to base the script logic, hence, in order to bypass this problem a combination of scrapy and selenium was used to crawl and scrape the 4 web pages in this project (2 court instances for each)

- Regex was vastly used since some CSS could be in many sorts of formats
