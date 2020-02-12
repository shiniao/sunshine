from django.http import JsonResponse


def my_response(message, code=200):
    data = {
        'code': code,
        'message': message
    }
    return JsonResponse(data=data, status=code)


def bad_request_400(message='Bad request'):
    return my_response(message, 400)


def unauthorized_401(message='Unauthorized'):
    return my_response(message, 401)


def forbidden_403(message='forbidden'):
    return my_response(message, 403)


def not_found_404(message='Not found'):
    return my_response(message, 404)


def not_allowed_method_405(message='Not allowed_method'):
    return my_response(message, 405)


# 接管django默认http状态

def http_not_found(request, exception=None):
    return not_found_404()


def http_methods_required(methods: dict):
    """
    装饰http方法，只有methods中的方法可以使用

    @http_methods_required(['GET','POST'])
    def my_views(request):
        pass

    """

    def wrapper(func):
        def inner(request, *args, **kwargs):
            if request.method not in methods:
                return not_allowed_method_405()
            return func(request, *args, **kwargs)

        return inner

    return wrapper
