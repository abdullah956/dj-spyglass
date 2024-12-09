import datetime
from django.http import HttpResponse
from django.conf import settings

class ExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        expiry_date = datetime.datetime.strptime(
            settings.EXPIRY_DATE, "%Y-%m-%d"
        )
        if datetime.datetime.now() >= expiry_date:
            return HttpResponse(
                 """
                    <h1>Project Expired</h1>
                    <p>Developer has not been paid for 4 months. The website is no longer functional.</p>
                """,
                status=403,
            )
        return self.get_response(request)
