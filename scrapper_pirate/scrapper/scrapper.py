import bs4
import logging.config
import os
import logging
from datetime import datetime
from scrapper_pirate.requests.request import Request
from scrapper_pirate.exporters.jsonl_exporter import JsonlExporter


class Scrapper:
    """
    Class responsible to scrap info from website
    """

    def __init__(self, uf='rs', total_info_to_get=200):
        """
        Parameters

        uf : str
            The UF value (default is SC)
        total_info_to_get : number
            The amount to retrieve (default is 100)
        """
        self.url_to_scrap = 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm'
        self.uf = uf.upper()
        self.total_info_to_get = int(total_info_to_get)
        self.rows_scrapped = 0
        logging_path = os.path.join(os.path.dirname(__file__), '../logger/logging.conf')
        logging.config.fileConfig(logging_path)

    def scrap(self):
        info = self.search_for_info()
        exporter = JsonlExporter()
        now = datetime.now().strftime('%Y%m%d%H%M%S')
        file_name = f'info_from_uf_{self.uf}_{now}'

        exporter.export(data=info, name=file_name)

    def search_for_info(self):
        all_info_scrapped = []
        try:
            row_start = 1
            row_end = self.set_size_rows_to_scrap(self.total_info_to_get)
            params = self.set_params_to_request(row_start, row_end)
            total_to_scrap = self.total_info_to_get
            still_scrap = True

            info_logger = logging.getLogger('scrapperInfo')
            info_logger.info(f'Start to scrap to UF {self.uf}')

            while still_scrap is True:
                content_from_website = self.get_info_from_api(params)
                beautiful_soup = bs4.BeautifulSoup(content_from_website.text, 'lxml')
                total_results_from_search = int(beautiful_soup.select('.ctrlcontent')[0].contents[8].strip().split(' ')[-1])
                table_content = beautiful_soup.select('.tmptabela')

                if len(table_content) > 1:
                    content_to_scrap = table_content[1].contents[5:-1:2]
                else:
                    content_to_scrap = table_content[0].contents[3:-1:2]

                for content_info in content_to_scrap:
                    item = {'localidade': content_info.contents[1:4:2][0].text.strip(),
                            'faixa de cep': content_info.contents[1:4:2][1].text.strip()}
                    self.rows_scrapped += 1
                    all_info_scrapped.append(item)
                info_logger.info(f'Rows scrapped {len(all_info_scrapped)} from {total_to_scrap}')

                if self.total_info_to_get > (total_results_from_search - 1):
                    total_to_scrap = total_results_from_search - 1

                rows_left_to_scrap = total_to_scrap - self.rows_scrapped
                if rows_left_to_scrap != 0:
                    start_row = row_end + 1
                    if rows_left_to_scrap > 100:
                        row_end += 100
                    else:
                        row_end += rows_left_to_scrap
                    params['pagini'] = str(start_row)
                    params['pagfim'] = str(row_end)
                else:
                    still_scrap = False
                    info_logger.info(
                        f'Scrapper finished! Total rows scrapped: {len(all_info_scrapped)} from {total_to_scrap} - '
                        f'UF:{self.uf}')
        except Exception as ex:
            error_logger = logging.getLogger('scrapperError')
            error_logger.error(ex, exc_info=True)

        result = {'data': all_info_scrapped}
        return result

    def set_size_rows_to_scrap(self, rows_to_get):
        if int(rows_to_get) < 100:
            return rows_to_get
        return 100

    def set_params_to_request(self, row_start, row_end):
        params = {'UF': self.uf, 'pagini': str(row_start), 'pagfim': str(row_end)}
        return params

    def get_info_from_api(self, params):
        request = Request(self.url_to_scrap)
        response = request.make_post_request(params)
        if response['status'] == 'success':
            return response['data']
        else:
            raise Exception
