from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AdminUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='', related_name='adminUser')
    
    def __str__(self) -> str:
        return self.user.username