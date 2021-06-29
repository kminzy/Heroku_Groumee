from django.db import models

# Create your models here.
class User(models.Model):
    userId=models.CharField(max_length=50)
    password=models.CharField(max_length=150)
    name=models.CharField(max_length=10)

class Schedule(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default='')
    start=models.DateTimeField
    end=models.DateTimeField
    title=models.CharField(max_length=60)

class Group(models.Model):
    name=models.CharField(max_length=50)
    leader=models.ForeignKey(User,on_delete=models.CASCADE,default='')

class UserGroup(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default='')
    group=models.ForeignKey(Group,on_delete=models.CASCADE,default='')

class GroupSchedule(models.Model):
    group=models.ForeignKey(UserGroup,on_delete=models.CASCADE,default='')
    start=models.DateTimeField
    end=models.DateTimeField
    title=models.CharField(max_length=60)

