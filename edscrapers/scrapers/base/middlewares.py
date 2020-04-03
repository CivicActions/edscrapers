import re
from scrapy.spidermiddlewares.offsite import OffsiteMiddleware

class RegexOffsiteMiddleware(OffsiteMiddleware):
    def get_host_regex(self, spider):

        allowed_domains = getattr(spider, 'allowed_domains', None)

        if allowed_domains:
            regex = r'^(.*\.)?(%s)$' % '|'.join(re.escape(d) for d in allowed_domains if d is not None)
        else:
            return re.compile('') # allow all by default

        allowed_regex = getattr(spider, 'allowed_regex', None)
        if allowed_regex:
            return re.compile(allowed_regex)
        else:
            return re.compile(regex)
