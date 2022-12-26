from django.http import HttpResponse

from .tasks import send_feedback_email_task

def test_task(request):
    send_feedback_email_task.delay(email_address='sarifin439@gmail.com', message="This is an EXPERIMENTAL MESSAGE from ECOMMERCE APP!")
    return HttpResponse('response done')