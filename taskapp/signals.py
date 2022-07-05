from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import *
import uuid

@receiver(pre_save,sender=User)
def create_patient_id(sender,instance,**kwargs):
    if instance.id in [None,""]:
        count = User.objects.count()
        id = str(uuid.uuid4())[:7] + str(count+1)[:1]
        pat=User.objects.filter(id=id)
        while pat.exists():
            id = str(uuid.uuid4())[:7] + str(count+1)[:1]
        instance.id=id 

@receiver(pre_save,sender=Task)
def create_patient_id(sender,instance,**kwargs):
    if instance.id in [None,""]:
        count = Task.objects.count()
        id = str(uuid.uuid4())[:7] + str(count+1)[:1]
        pat=Task.objects.filter(id=id)
        while pat.exists():
            id = str(uuid.uuid4())[:7] + str(count+1)[:1]
        instance.id=id 
