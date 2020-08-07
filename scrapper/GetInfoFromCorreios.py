import requests
import bs4
import jsonlines
import sys
from datetime import datetime


def getInfo(total_rows_to_get=200, uf='RS', localidade=''):
    url = 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm'
    scrapped_rows = 0
    start_row = 1
    final_row = 100 if total_rows_to_get > 100 else total_rows_to_get
    params = {'UF': uf.upper(), 'Localidade': localidade,  'pagini': str(start_row), 'pagfim': str(final_row)}

    result = []
    still_scrap = True
    need_check_total_rows = True

    while still_scrap is True:
        response = requests.post(url, data=params)
        soup = bs4.BeautifulSoup(response.text, 'lxml')

        #total_results_from_search = str(soup.select('.ctrlcontent')[0].contents[8]).strip().split(' ')[-1]
        total_results_from_search = soup.select('.ctrlcontent')[0].contents[8].strip().split(' ')[-1]

        if len(soup.select('.tmptabela')) > 1:
            all_table = soup.select('.tmptabela')[1].contents
            ufs_table = all_table[5:-1:2]
        else:
            all_table = soup.select('.tmptabela')[0].contents
            ufs_table = all_table[3:-1:2]

        for ufs_info in ufs_table:
            item = {'localidade': ufs_info.contents[1:4:2][0].text.strip(),
                    'faixa de cep': ufs_info.contents[1:4:2][1].text.strip()}
            scrapped_rows += 1
            result.append(item)

        rows_left = total_rows_to_get - scrapped_rows
        if rows_left != 0:
            start_row = final_row + 1
            if rows_left > 100:
                final_row += 100
            else:
                final_row += rows_left
            params['pagini'] = str(start_row)
            params['pagfim'] = str(final_row)
        else:
            still_scrap = False

        if need_check_total_rows is True and total_rows_to_get > int(total_results_from_search):
            if scrapped_rows == int(total_results_from_search) - 1:
                still_scrap = False
            else:
                total_rows_to_get = int(total_results_from_search) - 1
                need_check_total_rows = False
    ceps = {'ceps': result}
    return ceps


def transformToJsonl(info, uf_name):
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    with jsonlines.open(f"info_from_uf_{uf_name}_{now}.jsonl", mode='w') as writer:
        for i in info['ceps']:
            writer.write(i)


def execute(uf, total=200, localidade=''):
    res = getInfo(total, uf, localidade)
    transformToJsonl(res, uf)


if __name__ == '__main__':
    uf_to_search = sys.argv[1]
    if len(sys.argv) > 1:
        rows_to_get = sys.argv[2]
        execute(uf_to_search, int(rows_to_get))
    else:
        execute(uf_to_search)
