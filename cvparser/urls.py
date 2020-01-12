from django.urls import path
from cvparser.views import home

urlpatterns = [
    path("", home, name='index'),
]