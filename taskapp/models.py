from django.db import models

# Create your models here.
class User(models.Model):
    id = models.CharField(max_length=256,primary_key=True,unique=True,editable=False)
    name = models.CharField(max_length=256,null=True,blank=True)
    email = models.CharField(max_length=256,null=True,blank=True,unique=True)
    password = models.CharField(max_length=256,null=True,blank=True)
    phone = models.CharField(max_length=256,null=True,blank=True,unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}-{self.id}"

class Task(models.Model):
    id = models.CharField(max_length=256,primary_key=True,unique=True,editable=False)
    user_id = models.CharField(max_length=256,null=True,blank=True,editable=False)
    title = models.CharField(max_length=1024,null=True,blank=True)
    content  = models.TextField(null=True,blank=True)
    start_time = models.TimeField(null=True,blank=True)
    end_time = models.TimeField(null=True,blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.title}-{self.id}"
