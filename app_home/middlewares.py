from django.shortcuts import get_object_or_404, redirect,render


class UnderConstructionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # response = self.get_response(request)
        response = render(request, 'underConstruction.html')

        # Code to be executed for each request/response after
        # the view is called.

        return response