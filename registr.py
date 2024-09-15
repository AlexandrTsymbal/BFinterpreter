from functools import wraps


def registr(command):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        if not hasattr(wrapper, "_registry"):
            wrapper._registry = {}

        command_registry[command] = wrapper
        return wrapper

    return decorator


command_registry = {}
