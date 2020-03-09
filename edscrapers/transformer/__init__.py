import logging

from datetime import datetime

log_file_name = 'transformer-{}.log'.format(datetime.now().isoformat())
logging.basicConfig(filename=log_file_name,level=logging.DEBUG)
logger = logging.getLogger(__name__)