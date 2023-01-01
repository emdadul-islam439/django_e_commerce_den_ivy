import json
from django.db import models
from django.utils import timezone
from django_enum_choices.fields import EnumChoiceField
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from .enums import TimeInterval, SetupStatus
from store.models import Order
# from .signals import create_or_update_periodic_task

class EmailSendingTask(models.Model):
    # title = models.CharField(max_length=70, blank=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='order')
    status = EnumChoiceField(SetupStatus, default=SetupStatus.active)
    time_interval = EnumChoiceField(TimeInterval, default=TimeInterval.five_mins)
    # experimental_task = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE, null=True, blank=True, related_name='experimental_task')
    immediate_email = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE, null=True, blank=True, related_name='immediate_task')
    scheduled_email = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE, null=True, blank=True, related_name='scheduled_task')
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
    
    # def setup_experimental_task(self):
    #     self.experimental_task = PeriodicTask.objects.create(
    #         name=self.title,
    #         task='computation_heavy_task',
    #         interval=self.interval_schedule,
    #         args=json.dumps([self.id]),
    #         start_time=timezone.now()
    #     )
    #     self.save(update_fields=['experimental_task'])
        
    def send_immediate_email(self):
        self.immediate_email = PeriodicTask.objects.create(
            name=f'Immediate Email TASK of ORDER-> {self.order.id}',
            task='only_celery_app.tasks.send_feedback_email_task',
            one_off=True,
            interval=IntervalSchedule.objects.get(every=1, period='seconds'),
            args=json.dumps(['sarifin439@gmail.com', 'Hi this is the IMMEDIATE Email.... Please keep me in touch.']),
            start_time=timezone.now()
        )
        self.save(update_fields=['scheduled_task'])
    
    def create_scheduled_email(self):
        self.scheduled_email = PeriodicTask.objects.create(
            name=f'Scheduled Email TASK of ORDER-> {self.order.id}',
            task='only_celery_app.tasks.send_feedback_email_task',
            one_off=True,
            interval=IntervalSchedule.objects.get(every=1, period='minutes'),
            args=json.dumps(['sarifin439@gmail.com', 'Hi this is the SCHEDULED Email.... Please keep me in touch.']),
            start_time=timezone.now()
        )
        self.save(update_fields=['scheduled_task'])
        
    def disable_scheduled_email(self):
        self.scheduled_email.enabled = False
        self.save(update_fields=['scheduled_task'])
        
    def enable_scheduled_email(self):
        self.scheduled_email.enabled = True
        self.save(update_fields=['scheduled_task'])
    
    
    #TODO: COULD NOT BE SUCCESSFUL IN THIS FUNCTION, 
    #TODO: PROBLEM-> "Exception Value: maximum recursion depth exceeded while calling a Python object" 
    # def delete_related_tasks(self, *args, **kwargs):
    #     print("DELETING ALL THE TASKS.......................................")
    #     if self.experimental_task is not None:
    #         self.experimental_task.delete()
            
    #     if self.immediate_task is not None:
    #         self.immediate_task.delete()
            
    #     if self.scheduled_task is not None:
    #         self.scheduled_task.delete()    