from functools import wraps

def exempt_from_my_authentication_middleware(view_func):
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.my_exempt_flag = True
    return wraps(view_func)(wrapped_view)