from time import sleep
from django.core.mail import send_mail
from celery import shared_task

# from .models import Setup

@shared_task()
def send_feedback_email_task(email_address, message):
    """Sends an email when the feedback form has been submitted."""
    sleep(10)  # Simulate expensive operation(s) that freeze Django
    send_mail(
        "Your Feedback",
        f"\t{message}\n\nThank you!",
        "support@example.com",
        [email_address],
        fail_silently=False,
    )
    
# @shared_task(name="computation_heavy_task")
# def computation_heavy_task(setup_id):
#     setup = Setup.objects.get(id=setup_id)
#     # Do heavy computation with variables in setup model here.
#     print('''Running task for setup {setup_title}.'''.format(
#         setup_title=setup.title))