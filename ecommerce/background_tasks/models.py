import json
from django.db import models
from django.utils import timezone
from django_enum_choices.fields import EnumChoiceField
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from .enums import TimeInterval, SetupStatus
from store.models import Order
# from .signals import create_or_update_periodic_task

class EmailSendingTask(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='order')
    status = EnumChoiceField(SetupStatus, default=SetupStatus.active)
    time_interval = EnumChoiceField(TimeInterval, default=TimeInterval.five_mins)
    immediate_email = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE, null=True, blank=True, related_name='immediate_email')
    scheduled_email = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE, null=True, blank=True, related_name='scheduled_email')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'EmailSendingTask'
        verbose_name_plural = 'EmailSendingTasks'
            
    def __str__(self) -> str:
        return f'EmailSendingTask: Order = {self.order}'
            
    @property
    def interval_schedule(self):
        if self.time_interval == TimeInterval.one_min:
            return IntervalSchedule.objects.get(every=1, period='minutes')
        if self.time_interval == TimeInterval.five_mins:
            return IntervalSchedule.objects.get(every=5, period='minutes')
        if self.time_interval == TimeInterval.one_hour:
            return IntervalSchedule.objects.get(every=1, period='hours')
        raise NotImplementedError
    
    def send_immediate_email(self, order_id, recipient_email):
        self.immediate_email = PeriodicTask.objects.create(
            name=f'Immediate Email TASK of ORDER-> {self.order.id}',
            task='background_tasks.tasks.send_order_creation_email',
            one_off=True,
            interval=IntervalSchedule.objects.get(every=1, period='seconds'),
            args=json.dumps([order_id, recipient_email]),
            start_time=timezone.now()
        )
        self.save(update_fields=['immediate_email'])
    
    def create_scheduled_email(self, order_id, recipient_email):
        self.scheduled_email = PeriodicTask.objects.create(
            name=f'Scheduled Email TASK of ORDER-> {self.order.id}',
            task='background_tasks.tasks.cancel_order_and_send_email',
            one_off=True,
            interval=IntervalSchedule.objects.get(every=2, period='minutes'),
            args=json.dumps([order_id, recipient_email, self.id]),
            start_time=timezone.now()
        )
        self.save(update_fields=['scheduled_email'])
        
    def cancel_order(self):
        print(f'Cancelling order')
        self.order.order_status = 5 # order_status = cancelled
        self.order.save()
        
    def disable_scheduled_email(self):
        print(f'Disabling scheduled email...')
        self.scheduled_email.enabled = False
        self.scheduled_email.save()
        
    def enable_scheduled_email(self):
        print(f'Enabling scheduled email...')
        self.scheduled_email.enabled = True
        self.scheduled_email.save()
    
    #TODO: COULD NOT BE SUCCESSFUL IN THIS FUNCTION, 
    #TODO: PROBLEM-> "Exception Value: maximum recursion depth exceeded while calling a Python object" 
    # def delete_related_tasks(self, *args, **kwargs):
    #     print("DELETING ALL THE TASKS.......................................")
    #     if self.experimental_task is not None:
    #         self.experimental_task.delete()
            
    #     if self.immediate_task is not None:
    #         self.immediate_task.delete()
            
    #     if self.scheduled_email is not None:
    #         self.scheduled_email.delete()    