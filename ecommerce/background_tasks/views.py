from django.http import HttpResponse

from .tasks import send_order_creation_email

def test_task(request):
    send_order_creation_email.delay(email_address='sarifin439@gmail.com', message="This is an EXPERIMENTAL MESSAGE from ECOMMERCE APP!")
    return HttpResponse('response done')