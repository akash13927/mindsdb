import importlib
from mindsdb.utilities.log import get_log
logger = get_log(logger_name="main")


def action_logger(logger, loglevel="info"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            log_func = getattr(logger, loglevel)
            instance = args[0]
            log_func("%s.%s: calling with args - %s, kwargs - %s", instance.__class__.__name__, func.__name__, args[1:], kwargs)
            res = func(*args, **kwargs)
            log_func("%s.%s: returning - %s", instance.__class__.__name__, func.__name__, res)
            return res
        return wrapper
    return decorator


def get_handler(_type):
    _type = _type.lower()
    # a crutch to fix bug in handler naming convention
    if _type == "files":
        _type = "file"
    handler_folder_name = _type + "_handler"
    logger.debug("get_handler: handler_folder - %s", handler_folder_name)

    try:
        handler_module = importlib.import_module(f'mindsdb.integrations.handlers.{handler_folder_name}')
        logger.debug("get_handler: handler module - %s", handler_module)
        handler = handler_module.Handler
        if handler is None:
            logger.error("get_handler: import error - %s", handler_module.import_error)
        logger.debug("get_handler: found handler - %s", handler)
        return handler
    except Exception as e:
        raise e
