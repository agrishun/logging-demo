import unittest
import logging
import logging.config
from multiprocessing import Pool
from unittest.mock import patch, mock_open, call
from time import sleep

logging_config = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(message)s'
        }
    },
    'handlers': {
        'file': {
            'class': 'logger.MultiprocessLogger',
            'filename': 'logs.log',
            'level': 'INFO',
            'formatter': 'simple',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    },
}


def test(value):
    logger = logging.getLogger()
    logger.info(value)


class TestMultiprocessLogger(unittest.TestCase):
    def test_multiprocess_logging(self):

        m = mock_open()
        with patch('builtins.open', m, create=True):
            logging.config.dictConfig(logging_config)

            test('main_start')
            p = Pool(3)
            p.map(test, [1, 2, 3])
            test('main_end')

        sleep(0.1)
        m.assert_called_once()

        filehandle = m()
        filehandle.write.assert_has_calls(map(call, [
            'main_start\n',
            '1\n',
            '2\n',
            '3\n',
            'main_end\n'
        ]), any_order=True)
        assert filehandle.write.call_count == 5


if __name__ == '__main__':
    unittest.main()
