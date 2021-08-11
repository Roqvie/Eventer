import peewee


def syncErrorHandler(func):

    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except peewee.DoesNotExist:
            return None

    return wrapper


