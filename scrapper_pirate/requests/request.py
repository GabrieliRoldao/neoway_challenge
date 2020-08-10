import requests
import logging.config
import os


class Request:

    def __init__(self, url):
        self.url = url
        logging_path = os.path.join(os.path.dirname(__file__), '../logger/logging.conf')
        logging.config.fileConfig(logging_path)
        self.logger = logging.getLogger('requestError')

    def make_post_request(self, params):
        response = None
        try:
            response = requests.post(self.url, data=params)
            return {'status': 'success', 'data': response}
        except requests.exceptions.HTTPError as e:
            self.logger.error(e)
            return {'status': 'error', 'data': response, 'message': 'Sorry, but an error has occured.'}
