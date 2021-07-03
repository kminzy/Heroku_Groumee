from django.db import models

# Create your models here.

class User(models.Model):   
    userId=models.CharField(max_length=50,primary_key=True) 
    password=models.CharField(max_length=150)
    name=models.CharField(max_length=10)

class Group(models.Model):
    name=models.CharField(max_length=50)
    members=models.ManyToManyField('User',related_name="groups")
    leader=models.ForeignKey(User,on_delete=models.CASCADE,default='')

'''
#UserGroup은 User와 Group의 중개 모델
class UserGroup(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default='')
    group=models.ForeignKey(Group,on_delete=models.CASCADE,default='')
'''

#하나의 일정
class Schedule(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default='')
    start=models.DateTimeField()
    end=models.DateTimeField()
    title=models.CharField(max_length=60)

class GroupSchedule(models.Model):
    group=models.ForeignKey(Group,on_delete=models.CASCADE,default='')
    start=models.DateTimeField()
    end=models.DateTimeField()
    title=models.CharField(max_length=60)  
