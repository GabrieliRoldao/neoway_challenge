# Data Pirates challenge

Scrapper project that get info from [Correios](http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm) and export 
to JSONL file.

**Requirements**

This project runs on `Python 3.8`.

To install all requirements, execute: 
    
    $ pip install -r requirements.txt

**Run project**

To execute in console, run:
    
    $ python app.py sc 200

Where `sc` is the UF name to get info and `200` is the total amount to get from scrapper.

The default value for `uf` is `SP` and for `total_items` is `200`  

To run this application as a docker container, run:

    $ docker run --rm --name scrapper \
        -v ~/scrapper/files_exported:/app/scrapper_pirate/files/ \
        -v ~/scrapper/logs:/app/scrapper_pirate/logs \
        -e UF=RS \
        -e ITEMS=350 \
        gabrieliroldao/scrapper_pirate:1.0.0


**Run unit tests**

To run unit tests, run:
    
    $ cd tests/scrapper
    $ python scrapper_test.py 
    

Xoxo