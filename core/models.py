from django.db import models
import uuid
from accounts.models import User
# Create your models here.
class Collections(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)


class HandwritingInputLogger(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    collection = models.ForeignKey(Collections,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    input_file = models.FileField(upload_to='inputFiles/')
    status = models.BooleanField(default=False)
    error_status = models.BooleanField(default=False)
    error_logger = models.CharField(max_length=100,default='No error')


class OutputFiles(models.Model):
    input_details = models.OneToOneField(HandwritingInputLogger,on_delete=models.CASCADE)
    url = models.CharField(max_length=255)