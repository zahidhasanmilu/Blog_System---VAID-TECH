from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model

User = get_user_model()


# class UnderConstructionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         # One-time configuration and initialization.

#     def __call__(self, request):
#         # Code to be executed for each request before
#         # the view (and later middleware) are called.

#         # response = self.get_response(request)
#         response = render(request, 'underConstruction.html')

#         # Code to be executed for each request/response after
#         # the view is called.

#         return response


class UnderConstructionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #  path under construction
        under_construction_paths = [
            "/tag/inheritance/",
        ]  # example paths

        if request.path in under_construction_paths:
            return render(request, "underConstruction.html")

        # other request normal response
        response = self.get_response(request)
        return response
