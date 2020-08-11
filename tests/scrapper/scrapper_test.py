import unittest
import sys
import os, glob
import mock
import bs4

sys.path.insert(0, os.path.dirname('../../scrapper_pirate'))
from scrapper_pirate.scrapper.correios_scrapper import CorreiosScrapper
from pathlib import Path

files_with_110_items = ['scrapper_pirate/resources/first_page_with_100_from_110_items.html',
                        'scrapper_pirate/resources/next_page_with_10_from_110_items.html']
files_with_110_items.reverse()

file_with_1_item = 'scrapper_pirate/resources/first_page_with_1_item.html'
file_with_100_item = 'scrapper_pirate/resources/first_page_with_100_items.html'

files_open = []


class ScrapperTest(unittest.TestCase):

    def setUp(self):
        self.__remove_files()

    def tearDown(self):
        self.__close_files()
        self.__remove_files()

    def test_scrap_with_110_items(self):
        final_file_name = 'test_scrap_with_110_items'
        scrapper_with_two_pages = CorreiosScrapper(uf='sc', total_items=110)
        scrapper_with_two_pages.exporter.folder_path = 'scrapper_pirate/files/'
        params = {'UF': scrapper_with_two_pages.uf, 'pagini': str(1), 'pagfim': str(100)}
        scrapper_with_two_pages.build_beautiful_soup = mock.Mock()
        scrapper_with_two_pages.build_beautiful_soup.side_effect = [self.__mock_beautiful_soup_110_items(params),
                                                                    self.__mock_beautiful_soup_110_items(params)]
        scrapper_with_two_pages.scrap(file_to_export=final_file_name)
        self.__close_files()

        file_path = 'scrapper_pirate/files/' + final_file_name + '.jsonl'
        self.assertTrue(self.__is_file_exists(file_path))
        self.assertEqual(110, self.__count_rows_from_file(file_path))

        if self.__is_file_exists(file_path):
            os.remove(file_path)

    def test_scrap_with_1_item(self):
        scrapper_with_one_item = CorreiosScrapper(uf='sc', total_items=1)
        final_file_name = 'test_scrap_with_1_items'
        scrapper_with_one_item.exporter.folder_path = 'scrapper_pirate/files/'
        params = {'UF': scrapper_with_one_item.uf, 'pagini': str(1), 'pagfim': str(100)}
        scrapper_with_one_item.build_beautiful_soup = mock.Mock()
        scrapper_with_one_item.build_beautiful_soup.side_effect = [self.__mock_beautiful_soup_1_item(params)]
        scrapper_with_one_item.scrap(file_to_export=final_file_name)
        self.__close_files()

        file_path = 'scrapper_pirate/files/' + final_file_name + '.jsonl'
        self.assertTrue(self.__is_file_exists(file_path))
        self.assertEqual(1, self.__count_rows_from_file(file_path))

        if self.__is_file_exists(file_path):
            os.remove(file_path)

    def test_scrap_with_100_item(self):
        scrapper_with_one_hundred_item = CorreiosScrapper(uf='sc', total_items=100)
        final_file_name = 'test_scrap_with_100_items'
        scrapper_with_one_hundred_item.exporter.folder_path = 'scrapper_pirate/files/'
        params = {'UF': scrapper_with_one_hundred_item.uf, 'pagini': str(1), 'pagfim': str(100)}
        scrapper_with_one_hundred_item.build_beautiful_soup = mock.Mock()
        scrapper_with_one_hundred_item.build_beautiful_soup.side_effect = \
            [self.__mock_beautiful_soup_100_item(params)]
        scrapper_with_one_hundred_item.scrap(file_to_export=final_file_name)
        self.__close_files()

        file_path = 'scrapper_pirate/files/' + final_file_name + '.jsonl'
        self.assertTrue(self.__is_file_exists(file_path))
        self.assertEqual(100, self.__count_rows_from_file(file_path))

        if self.__is_file_exists(file_path):
            os.remove(file_path)

    def test_scrap_with_200_items_over_100_items(self):
        scrapper_with_two_hundred_item = CorreiosScrapper(uf='sc', total_items=200)
        final_file_name = 'test_scrap_with_200_items_over_100_items'
        scrapper_with_two_hundred_item.exporter.folder_path = 'scrapper_pirate/files/'
        params = {'UF': scrapper_with_two_hundred_item.uf, 'pagini': str(1), 'pagfim': str(100)}
        scrapper_with_two_hundred_item.build_beautiful_soup = mock.Mock()
        scrapper_with_two_hundred_item.build_beautiful_soup.side_effect = \
            [self.__mock_beautiful_soup_100_item(params)]
        scrapper_with_two_hundred_item.scrap(file_to_export=final_file_name)
        self.__close_files()

        file_path = 'scrapper_pirate/files/' + final_file_name + '.jsonl'
        self.assertTrue(self.__is_file_exists(file_path))
        self.assertEqual(100, self.__count_rows_from_file(file_path))

        if self.__is_file_exists(file_path):
            os.remove(file_path)

    def __mock_beautiful_soup_110_items(self, params):
        file = files_with_110_items.pop()
        file_open = open(file)
        files_open.append(file_open)
        return bs4.BeautifulSoup(file_open, "html.parser")

    def __mock_beautiful_soup_1_item(self, params):
        file_open = open(file_with_1_item)
        files_open.append(file_open)
        return bs4.BeautifulSoup(file_open, "html.parser")

    def __mock_beautiful_soup_100_item(self, params):
        file_open = open(file_with_100_item)
        files_open.append(file_open)
        return bs4.BeautifulSoup(file_open, "html.parser")

    def __is_file_exists(self, file_name):
        final_file = Path(file_name)
        return final_file.is_file()

    def __count_rows_from_file(self, file):
        with open(file) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def __close_files(self):
        for file in files_open:
            file.close()

    def __remove_files(self):
        file_path = 'scrapper_pirate/files/*'
        files_to_remove = glob.glob(file_path)
        for file in files_to_remove:
            os.remove(file)


if __name__ == '__main__':
    unittest.main()
