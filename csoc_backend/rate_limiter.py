from ratelimit.decorators import ratelimit
from django.http import HttpResponseForbidden

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = ratelimit(key='ip', rate='100/s', block=True)(self.get_response)(request)
        if getattr(request, 'limited', False):
            return HttpResponseForbidden('Too Many Requests')

        return response
