from django.http import JsonResponse


def my_response(message, code=200):
    data = {
        'code': code,
        'message': message
    }
    return JsonResponse(data=data, status=code)
