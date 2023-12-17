import random
import logging
import scrapy

from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.utils.python import global_object_name
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
from scrapy.exceptions import IgnoreRequest


class CustomHttpErrorMiddleware:
    def process_response(self, request, response, spider):
        if response.status in [400, 401, 403, 404, 406, 500, 502, 503, 504]:
            logging.info(f"Ignoring response {response}: HTTP status code is not handled or not allowed")
            return None
        return response

    def process_spider_exception(self, response, exception, spider):
        if isinstance(exception, IgnoreRequest):
            return None

        if isinstance(exception, HttpError):
            spider.logger.error(f"Received HttpError {exception} for {response.url}")
            return []

        if isinstance(exception, (DNSLookupError, TimeoutError, TCPTimedOutError)):
            spider.logger.error(f"Received {type(exception).__name__} for {response.url}")
            return [scrapy.Request(response.url, dont_filter=True)]

        return None


class RotateUserAgentMiddleware:
    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        user_agents = crawler.settings.getlist('USER_AGENTS')
        if not user_agents:
            raise ValueError("USER_AGENTS list is empty or not defined in settings.py")
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)


# Set the priority of the custom middleware lower than built-in ones to avoid conflicts
# with other middlewares that might rely on the response status code.
class CustomHttpErrorMiddlewarePriority:

    def __init__(self, priority):
        self.priority = priority

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        priority = settings.getint('HTTPERROR_MIDDLEWARE_PRIORITY') + 1
        return cls(priority)

    def process_request(self, request, spider):
        return None


# Set the priority of the custom middleware to rotate user agents higher than built-in ones
# to ensure it is applied before any other middlewares.
class RotateUserAgentMiddlewarePriority:

    def __init__(self, priority):
        self.priority = priority

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        priority = settings.getint('DOWNLOADER_MIDDLEWARES_PRIORITY') + 1
        return cls(priority)

    def process_request(self, request, spider):
        return None




