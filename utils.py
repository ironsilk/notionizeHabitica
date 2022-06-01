from functools import wraps


def error_wrap(f):
    """
    Used to raise error HTTP error when request status != 200
    :param f:
    :return:
    """
    print(f"Wrapped {f.__name__}", )

    @wraps(f)
    def wrap(*args, **kwargs):
        result = f(*args, **kwargs)
        print(result)
        if result.status_code != 200:
            result.raise_for_status()
        return result.json()

    return wrap