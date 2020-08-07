# Data Pirates challenge

Scrapper that get info from [here](http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm) and pass 
to JSONL file.

**Requirements**

This project runs on Python 3.8.

To install all requirements, execute `pip install -r requirements.txt`

**Run**

To execute this project, just run `python3 scrapper/get_info_from_correios.py uf rows_to_get` 

Where:
- uf: the uf you want to get info from
- rows_to_get: the number of rows you want to retrieve