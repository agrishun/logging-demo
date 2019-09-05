import os
import logging
import logging.config
from multiprocessing import Pool

logging_config = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(processName)-20s %(message)s'
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

logging.config.dictConfig(logging_config)
logger = logging.getLogger()

def test(value):
    msg = f'process {os.getpid()} message {value}'
    logger.info(msg)


def main():
    test('main_start')
    p = Pool(4)
    p.map(test, [1, 2, 3])
    test('main_end')


if __name__ == '__main__':
    main()
