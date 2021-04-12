from django.shortcuts import redirect
from django.urls import reverse
#装饰器函数
def login_decorator(session_item = 'is_login_manager', redirect_url = 'manager_login'):
    def decorator(func):
        def wrapper(request, *args, **kargs):
            if request.session.get(session_item,None):
                return func(request, *args, **kargs)
            else:
                return redirect(reverse(redirect_url))
        return wrapper
    return decorator