import logging

from Fitness.utils.background_scheduler import init_scheduler

logger = logging.getLogger("django")
try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x


class StartupMiddleware(object):
    def __init__(self, handler):
        # set up APScheduler
        logger.info('init scheduler')
        init_scheduler()

        from django.core.exceptions import MiddlewareNotUsed
        # Mission completed, raise this exception to remove this middle from Django MIDDLEWARE_CLASSES
        raise MiddlewareNotUsed
