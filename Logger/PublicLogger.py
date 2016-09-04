import logging
import time

current_date = str(int(time.strftime("%Y%m%d", time.localtime(time.time()))))
log_file_name = 'proxy_pool_log' + current_date + '.log'

# define the stream handler
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('ProxyPool')
logger.setLevel(logging.NOTSET)

log_handler = logging.FileHandler(log_file_name)
log_handler.setLevel(logging.DEBUG)

fmt = '%(asctime)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
log_formatter = logging.Formatter(fmt, datefmt)

log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)

print 'log finish!'