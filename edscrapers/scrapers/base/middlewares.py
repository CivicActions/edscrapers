import re
from scrapy.spidermiddlewares.offsite import OffsiteMiddleware

class RegexOffsiteMiddleware(OffsiteMiddleware):
    def get_host_regex(self, spider):
        allowed_regex = getattr(spider, 'allowed_regex', '')
        return re.compile(allowed_regex)
