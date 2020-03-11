import logging
from pathlib import Path
from datetime import datetime

Path(f"./log/").mkdir(parents=True, exist_ok=True)
log_file_name = './log/transformer-{}.log'.format(datetime.now().isoformat())
logging.basicConfig(filename=log_file_name,level=logging.DEBUG)
logger = logging.getLogger(__name__)
