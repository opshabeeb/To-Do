from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Userdetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=12)
    address=models.CharField(max_length=300)
    
    def __str__(self) :
        return str(self.user)
    
class Project(models.Model):
    title = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.title
    
class Todo(models.Model):
    STATUS_CHOICES = (
        ('pending', 'pending'),
        ('completed', 'completed'),
    )

    project = models.ForeignKey(Project, related_name='todos', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description
