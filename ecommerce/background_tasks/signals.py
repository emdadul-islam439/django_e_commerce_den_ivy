from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

from .models import EmailSendingTask
from .enums import SetupStatus

@receiver(post_save, sender=EmailSendingTask)
def create_or_update_periodic_task(sender, instance, created, **kwargs):
    print("IN SIGNALS.PY..................")
    if created:
        print("In SIGNALS.PY--->   IF CONDITION..........")
        instance.send_immediate_email(order_id=instance.order_id, recipient_email='sarifin439@gmail.com')
        instance.create_scheduled_email(order_id=instance.order_id, recipient_email='sarifin439@gmail.com')
    else:
        print("In SIGNALS.PY--->   ELSE CONDITION..........")
        if instance.scheduled_email is not None:
            if instance.status == SetupStatus.disabled and instance.scheduled_email.enabled is not False:
                instance.disable_scheduled_email()
            elif instance.status == SetupStatus.active and instance.scheduled_email.enabled is not True:
                # instance.enable_scheduled_email()
                pass
         
#TODO: COULD NOT BE SUCCESSFUL DELETING SETUP RELATED TASKS
#TODO: PROBLEM-> "Exception Value: maximum recursion depth exceeded while calling a Python object" 
# @receiver(pre_delete, sender=Setup)
# def delete_tasks(sender, instance, **kwargs):
#     print("in signals.py/delete_tasks()........................................")
#     if instance.experimental_task is not None or instance.immediate_task is not None or instance.scheduled_email is not None:
#         instance.delete_related_tasks() 
        