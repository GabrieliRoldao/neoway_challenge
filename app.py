import os
import logging.config
import sys
from scrapper_pirate.exceptions.negative_rows import NegativeRowsException
from scrapper_pirate.exceptions.args_out_range import ArgsOutRangeException
from scrapper_pirate.scrapper.scrapper import Scrapper

if __name__ == '__main__':
    logging_path = os.path.join(os.path.dirname(__file__), 'scrapper_pirate/logger/logging.conf')
    logging.config.fileConfig(logging_path)

    try:
        args = sys.argv
        if len(args) > 1:
            if len(args) > 3:
                raise ArgsOutRangeException(args[1:])
            if not int(args[2]):
                raise ValueError(args[2])
            if int(args[2]) < 0:
                raise NegativeRowsException(args[2])
            scrapper = Scrapper(uf=args[1], total_info_to_get=args[2])
        else:
            scrapper = Scrapper()
        scrapper.scrap()
    except NegativeRowsException as ex:
        error_logger = logging.getLogger('root')
        error_logger.error(ex)
    except ArgsOutRangeException as ex:
        error_logger = logging.getLogger('root')
        error_logger.error(ex)
    except ValueError as ex:
        error_logger = logging.getLogger('root')
        error_logger.error(f'The second arg is not a number type {ex.args}')

