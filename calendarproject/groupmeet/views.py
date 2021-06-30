from django.shortcuts import render, redirect,  get_object_or_404
from .models import User, Schedule, Group, GroupSchedule


#Calendar: 한달 단위 모든 일정
#Schedule: 일정 하나 하나

# Create your views here.

def userCalendar_view(request):
   return render(request, 'userCalendar.html')

def getuserGroupList(request,userId):
   user = get_object_or_404(User, id=userId)
   userGroup_list=list(user.groups.all())  #userid를 받아와서 user가 속한 usergroup 부르기
   return render(request,'userGroupList.html',{'userGroup_list':userGroup_list})

def addgroupSchedule(request,userlist):  #list를 인자로 받아와도 되는지?
   groupschedulelist=[]
   for user in userlist:
      schedule=Schedule.objects.filter(user=user)
      groupschedulelist.append(schedule)
   return render(request, 'groupCalendar.html',{'groupschedule_list':groupschedulelist})


