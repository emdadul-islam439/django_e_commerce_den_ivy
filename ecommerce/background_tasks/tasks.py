from time import sleep
from django.core.mail import send_mail
from celery import shared_task

from background_tasks.models import EmailSendingTask

@shared_task()
def send_order_creation_email(order_id, recipient_email):
    send_mail(
        "Please Complete Your Payment!",
        f"We have successfully received your order no. {order_id}. \nIf you did not complete your payment yet, please pay from the link below. Order will be expire soon! \n\nhttp://127.0.0.1:8000/order-details/{order_id} \n\nYou can also find your order details from this link. Thank you!",
        "support@ecommerce.com",
        [recipient_email],
        fail_silently=False,
    )   
     
@shared_task()
def cancel_order_and_send_email(order_id, recipient_email, email_sending_task_id):
    cancel_order(email_sending_task_id)
    send_order_cancellation_email(order_id, recipient_email)
    
def cancel_order(email_sending_task_id):
    emailSendingTask = EmailSendingTask.objects.get(id=email_sending_task_id)
    emailSendingTask.cancel_order()
    
def send_order_cancellation_email(order_id, recipient_email):
    send_mail(
        f"Order no. {order_id} is Cancelled!",
        f"Your order no. {order_id} is cancelled! \nYou can see the order details from the following link: \n\nhttp://127.0.0.1:8000/order-details/{order_id} \n\nThank you!",
        "support@ecommerce.com",
        [recipient_email],
        fail_silently=False,
    )
    
# @shared_task(name="computation_heavy_task")
# def computation_heavy_task(setup_id):
#     setup = Setup.objects.get(id=setup_id)
#     # Do heavy computation with variables in setup model here.
#     print('''Running task for setup {setup_title}.'''.format(
#         setup_title=setup.title))