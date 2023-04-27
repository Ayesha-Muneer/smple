from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Login(AbstractUser):
    is_worker = models.BooleanField(default=False)
    is_consumer = models.BooleanField(default=False)


class Worker(models.Model):
    user = models.OneToOneField(Login, on_delete=models.CASCADE, related_name='worker',null=True,blank=True)
    Name = models.CharField(max_length=100)
    Location = models.CharField(max_length=100)
    Contact_Number = models.CharField(max_length=10)
    Email = models.EmailField()
    Photo = models.FileField(upload_to='photo/')

    def __str__(self):
        return self.Name


class Consumer(models.Model):
    user = models.OneToOneField(Login, on_delete=models.CASCADE, related_name='consumer')
    Consumer_number = models.CharField(max_length=100)
    Name = models.CharField(max_length=100)
    Address = models.CharField(max_length=100)
    Mobile_Number = models.CharField(max_length=100)

    def __str__(self):
        return self.Name


class Schedule(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.DO_NOTHING)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.worker


# class Appointment(models.Model):
#     consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE,related_name='Appointment')
#     schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
#     Description = models.CharField(max_length=100)
#     Status = models.IntegerField(default=0)

class Appointment(models.Model):
    user = models.ForeignKey(Consumer, on_delete=models.CASCADE, related_name='appointment')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)


class Complaint(models.Model):
    user = models.ForeignKey(Login, on_delete=models.DO_NOTHING)
    subject = models.CharField(max_length=200)
    feedback = models.TextField()
    date = models.DateField()
    reply = models.TextField(null=True, blank=True)
