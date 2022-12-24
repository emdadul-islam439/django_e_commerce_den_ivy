from django.urls import path

from .views import index


urlpatterns = [
    path('celery-test/',index, name='celery_test_url'),
]