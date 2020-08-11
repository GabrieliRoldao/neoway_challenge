import bs4
import logging.config
import os
import logging
from datetime import datetime
from scrapper_pirate.requests.request import Request
from scrapper_pirate.exporters.jsonl_exporter import JsonlExporter
from scrapper_pirate.exceptions.uf_not_found import UfNotFound


class CorreiosScrapper:
    """
    Class responsible to scrap info from website
    """

    def __init__(self, uf='SP', total_items=200):
        """
        Parameters

        uf : str
            The UF value (default is SP)
        total_info_to_get : number
            The amount to retrieve (default is 200)
        """
        self.url_to_scrap = 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm'
        self.uf = uf.upper()
        self.total_items = int(total_items)
        self.rows_scrapped = 0
        self.total_to_scrap = self.total_items
        self.exporter = JsonlExporter()
        self.file_name = ''
        self.start_row = 1
        self.end_row = 100
        self.__create_files_dir_if_not_exists('../logs')
        logging_path = os.path.join(os.path.dirname(__file__), '../logger/logging.conf')
        logging.config.fileConfig(logging_path)
        self.info_logger = logging.getLogger('scrapperInfo')

    def scrap(self, file_to_export=None):
        """
        Method to execute scrapper

        Parameters

        file_to_export : str
            The path to export the scrapper result
        """
        try:
            info = self.__scrap_info()
            if len(info):
                if file_to_export is None:
                    self.file_name = self.__get_default_file_name()
                else:
                    self.file_name = file_to_export
                self.exporter.export(data=info, name=self.file_name)
                return True
        except Exception as ex:
            log_error = logging.getLogger('scrapperError')
            log_error.error(ex)
            return False

    def build_beautiful_soup(self, params):
        return bs4.BeautifulSoup(self.__get_info_from_api(params).text, 'lxml')

    def __get_default_file_name(self):
        now = datetime.now().strftime('%Y%m%d%H%M%s')
        return f'info_from_uf_{self.uf}_{now}'

    def __scrap_info(self):
        all_info_scrapped = []
        result = []
        try:
            self.start_row = 1
            row_start = 1
            row_end = self.__set_size_rows_to_scrap(self.total_items)
            params = self.__set_params_to_request(row_start, row_end)
            still_scrap = True

            self.info_logger.info(f'Start to scrap to UF {self.uf}')
            while still_scrap is True:
                beautiful_soup = self.build_beautiful_soup(params)
                if not self.__has_uf_info(beautiful_soup):
                    raise UfNotFound(self.uf)

                total_items_from_search = self.__get_total_items_from_search(beautiful_soup)
                if self.__total_items_is_greater_than_items_from_search(total_items_from_search):
                    self.total_items = total_items_from_search - 1

                table_content = self.__get_table_element(beautiful_soup)
                content_table = self.__get_content_from_table(table_content)
                all_info_scrapped += self.__scrap_infos_from_table(content_table)

                rows_left_to_scrap = self.total_items - self.rows_scrapped
                if rows_left_to_scrap > 0:
                    self.__go_to_next_page(rows_left_to_scrap, params)
                else:
                    still_scrap = False
                    self.info_logger.info(
                        f'Scrapper finished! Total rows scrapped: {len(all_info_scrapped)} from {self.total_to_scrap} - '
                        f'UF:{self.uf}'
                    )
            result = {'data': all_info_scrapped}
        except UfNotFound as ex:
            error_logger = logging.getLogger('scrapperError')
            error_logger.error(ex, exc_info=True)
        except Exception as ex:
            error_logger = logging.getLogger('scrapperError')
            error_logger.error(ex, exc_info=True)

        return result

    def __set_size_rows_to_scrap(self, rows_to_get):
        if int(rows_to_get) < 100:
            return rows_to_get
        return 100

    def __set_params_to_request(self, row_start, row_end):
        params = {'UF': self.uf, 'pagini': str(row_start), 'pagfim': str(row_end)}
        return params

    def __get_info_from_api(self, params):
        request = Request(self.url_to_scrap)
        response = request.make_post_request(params)
        if response['status'] == 'success':
            return response['data']
        else:
            raise Exception

    def __get_total_items_from_search(self, beautiful_soup):
        return int(beautiful_soup.select('.ctrlcontent')[0].contents[8].strip().split(' ')[-1])

    def __get_table_element(self, beautiful_soup):
        return beautiful_soup.select('.tmptabela')

    def __has_uf_info(self, beautiful_soup):
        if len(beautiful_soup.select('.tmptabela')) == 0:
            return False
        else:
            return True

    def __get_last_table(self, table_content):
        return table_content[1].contents[5:-1:2]

    def __get_first_table(self, table_content):
        return table_content[0].contents[3:-1:2]

    def __build_item(self, content_info):
        return {
            'localidade': content_info.contents[1:4:2][0].text.strip(),
            'faixa de cep': content_info.contents[1:4:2][1].text.strip()
        }

    def __total_items_is_greater_than_items_from_search(self, total_from_search):
        return self.total_items > (total_from_search - 1)

    def __get_content_from_table(self, table_content):
        if len(table_content) > 1:
            return self.__get_last_table(table_content)
        else:
            return self.__get_first_table(table_content)

    def __scrap_infos_from_table(self, content_to_scrap):
        all_info_scrapped = []
        for content_info in content_to_scrap:
            item = self.__build_item(content_info)
            self.rows_scrapped += 1
            all_info_scrapped.append(item)
        self.info_logger.info(f'Rows scrapped {len(all_info_scrapped)} from {self.total_items}')
        return all_info_scrapped

    def __go_to_next_page(self, rows_left_to_scrap, params):
        self.start_row = self.end_row + 1
        if rows_left_to_scrap > 100:
            self.end_row += 100
        else:
            self.end_row += rows_left_to_scrap
        params['pagini'] = str(self.start_row)
        params['pagfim'] = str(self.end_row)

    def __create_files_dir_if_not_exists(self, folder_path):
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)