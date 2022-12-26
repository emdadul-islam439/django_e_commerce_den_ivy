from django.urls import path

from .views import test_task


urlpatterns = [
    path('celery-test/', test_task, name='celery_test_url'),
]