from django.http import HttpResponse
from .webdriver import Webdriver


def webdriver_view(request):
    webdriver = Webdriver()
    webdriver.run()
    return HttpResponse('webdriver finished')
