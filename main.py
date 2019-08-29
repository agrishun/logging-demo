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
        'level': 'DEBUG',
        'handlers': ['file']
    },
}
logging.config.dictConfig(logging_config)


def func(value):
    logger = logging.getLogger(__name__)
    msg = f'process {os.getpid()} message {value}'
    logger.info(msg)


def main():
    func('start')
    p = Pool(4)
    p.map(func, [1, 2, 3, 4])
    func('end')


if __name__ == '__main__':
    main()
