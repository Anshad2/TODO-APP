from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title= models.CharField(max_length=200,unique=True)
    description= models.CharField(max_length=1000)
    priority_choices=[
        ('Low_priority','Low_priority'),
        ('Medium_priority','Medium_priority'),
        ('High_priority','High_priority')
    ]
    priority=models.CharField(max_length=200,choices=priority_choices,default='High_priority')
    due_date=models.DateField(null=True,blank=True)
    created_date=models.DateTimeField(auto_now_add=True,blank=True)
    completed=models.BooleanField(default=False)

    def _self_(self):
        return self.title