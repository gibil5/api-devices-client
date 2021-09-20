import logging
import re
import time
import typing

logger = logging.getLogger()


# Just for performance timing tests
def timed_request(method):

    def timed(*args, **kw):
        ts = time.time()
        try:
            uri = args[0].__dict__.get('base_url', '') + kw.get('resource_path', '')
        except IndexError:
            uri = kw.get('resource_path', '')

        logger.info(f'{method.__name__}({uri})')
        result = method(*args, **kw)
        te = time.time()
        response_time = (te - ts) * 1000
        logger.info(f'Response Time({uri})==>{response_time:2.2f} ms')

        return result

    return timed
