import discord_slash.error.IncorrectFormat


def syncErrorHandler(func):

    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except discord_slash.error.IncorrectFormat:
            return None

    return wrapper


