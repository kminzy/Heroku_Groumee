from django.db import models

# Create your models here.

class User(models.Model):   
    userId=models.CharField(max_length=50,primary_key=True) 
    password=models.CharField(max_length=150)
    name=models.CharField(max_length=10)

class Group(models.Model):
    name=models.CharField(max_length=50)
    members=models.ManyToManyField(User,through='UserGroup',through_fields=("group","user"))

#UserGroup은 User와 Group의 중개 모델
class UserGroup(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default='')
    group=models.ForeignKey(Group,on_delete=models.CASCADE,default='')
    allowed=models.IntegerField(default = 0)  
    #0:연관 없음, 1:초대했지만 수락하지 않음, 2:초대 후 수락 완료

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

class Comment(models.Model):
    writer=models.CharField(max_length=20)
    #writer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE) 로그인 완성되면 수정
    group= models.ForeignKey(Group ,on_delete=models.CASCADE,default='')
    pub_date = models.DateTimeField(default='')
    content = models.TextField(default='')