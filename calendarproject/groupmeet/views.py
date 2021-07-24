from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import render, redirect,  get_object_or_404
from .models import Schedule, Group, GroupSchedule, UserGroup, Comment
from account.models import CustomUser
from django.contrib.auth.decorators import login_required
import datetime
import calendar
from .calendar import (Calendar, UserCalendar)
from django.utils.safestring import mark_safe
import logging
import json
from django.core import serializers
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from .forms import UserScheduleCreationForm
from django.contrib import messages

#Calendar: 한달 단위 모든 일정
#Schedule: 일정 하나 하나
friend_list=[]

# Create your views here.
@login_required
def userCalendar_view(request):
   user = get_object_or_404(CustomUser, pk=request.user.nickname)

   today = get_date(request.GET.get('month'))
   prev_month_url = prev_month(today)
   next_month_url = next_month(today)
   
   cal = UserCalendar(today.year, today.month)
   cal = cal.formatmonth(withyear=True, user=user)
   cal = mark_safe(cal)

   form = UserScheduleCreationForm()
   
   return render(request, 'userCalendar.html', {
                           'calendar' : cal,
                           'cur_year' : today.year, 
                           'cur_month' : today.month, 
                           'prev_month' : prev_month_url, 
                           'next_month' : next_month_url,
                           'form' : form
                           })

@login_required
def show_userschedule(request):
   jsonObj = json.loads(request.body) #jsonObg.get('key')를 통해 접근가능, value들은 다 string형임

   year = int(jsonObj.get('year'))
   month = int(jsonObj.get('month'))
   day = int(jsonObj.get('day'))

   user = get_object_or_404(CustomUser, pk=request.user.nickname)
   date = datetime.date(year, month, day)

   schedules = Schedule.objects.filter(user=user, start__date__lte=date, end__date__gte=date).order_by('start')   # 유저가 클릭한 날짜에 있는 스케줄들

   data = serializers.serialize("json", schedules)                                                                # 스케줄들을 json형태로 바꿔줌

   return JsonResponse(data, safe=False)       # 파라미터로 딕셔너리 형태가 아닌 것을 받으면 두 번째 파라미터로 safe=False를 해야함

@login_required
def delete_userschedule(request):
   jsonObj = json.loads(request.body) #jsonObg.get('key')를 통해 접근가능, value들은 다 string형임
   pk = int(jsonObj.get('pk'))

   schedule = get_object_or_404(Schedule, pk=pk)
   schedule.delete()

   return JsonResponse(jsonObj)

@login_required
def create_userschedule(request):
   user = get_object_or_404(CustomUser, pk=request.user.nickname)
   new_schedule = Schedule(user=user)
   form = UserScheduleCreationForm(request.POST, instance=new_schedule)
   
   if form.is_valid():
      new_schedule = form.save()
      data = {
         'result' : 'success'
      }
      return JsonResponse(data)
   else:
      data = {
         'result' : 'fail',
         'form_errors' : form.errors.as_json()
      }
      return JsonResponse(data)
   

#사용자의 Id를 받아와서 사용자가 속한 group list return
def getuserGroupList(request):
   friend_list.clear()
   if request.user.is_authenticated:
      user = request.user
      usergroup=UserGroup.objects.filter(user=user)
      userGroup_list=[]
      for ug in usergroup:
         userGroup_list.append(ug.group)
      return render(request,'userGroupList.html',{'userGroup_list':userGroup_list})

# 그룹 캘린더 보여주기
def groupCalendar_view(request, id):            
   today = get_date(request.GET.get('month'))
   prev_month_url = prev_month(today)
   next_month_url = next_month(today)
   cur_month_url = "month=" + str(today.year) + '-' + str(today.month)
   # now = datetime.now()
   # cur_year = now.year        # 현재 연도
   # cur_month = now.month      # 현재 월

   group = Group.objects.get(id=id)
   cal = Calendar(today.year, today.month)
   cal = cal.formatmonth(withyear=True, group=group)
   cal = mark_safe(cal)

   members=[]
   testmembers= group.members.all()
   for testmember in testmembers:
      usergroups=UserGroup.objects.filter(user=testmember)
      for ug in usergroups:
         if (ug.allowed==2):
            members.append(testmember)

   #group에 속한 user들의 모든 일정 list로 return
   if request.GET.get('day'):
      day = request.GET.get('day')
   else:
      day = today.day
   schedule_list={'9':[0,0], '10':[0,0], '11':[0,0], '12':[0,0], '13':[0,0], '14':[0,0], '15':[0,0], '16':[0,0], '17':[0,0], '18':[0,0], '19':[0,0], '20':[0,0], '21':[0,0]}

   date_format = str(today.year)+"-"+str(today.month).zfill(2)+"-"+str(day).zfill(2)

   for user in members:
      schedules = Schedule.objects.filter(user=user, start__lte = date_format+" 22:00:00", end__gte = date_format+" 09:00:00")
      if schedules:
         for schedule in schedules:
            if schedule.start < datetime.datetime(int(today.year), int(today.month), int(day), 9, 0):
               s = 9
            else:
               if schedule.start.minute == 30:
                  schedule_list[str(schedule.start.hour)][1] = -1
               s = schedule.start.hour + 1 if schedule.start.minute == 30 else int(schedule.start.hour)
            if schedule.end > datetime.datetime(int(today.year), int(today.month), int(day), 22, 0):
               e = 21
            else:
               if schedule.end.minute == 30:
                  schedule_list[str(schedule.end.hour)][0] = -1
               e = schedule.end.hour - 1
            for i in range(s, e+1):
               schedule_list[str(i)][0] = -1
               schedule_list[str(i)][1] = -1
   groupSchedules = GroupSchedule.objects.filter(group=group, start__lte = date_format+" 22:00:00", end__gte = date_format+" 09:00:00")
   if groupSchedules:
      for schedule in groupSchedules:
         if schedule.start < datetime.datetime(int(today.year), int(today.month), int(day), 9, 0):
            s = 9
         else:
            if schedule.start.minute == 30:
                  schedule_list[str(schedule.start.hour)][1] = GroupSchedule.objects.get(id=schedule.id)
            s = schedule.start.hour+1 if schedule.start.minute == 30 else schedule.start.hour
            if schedule.end > datetime.datetime(int(today.year), int(today.month), int(day), 22, 0):
               e = 21
            else:
               if schedule.end.minute == 30:
                  schedule_list[str(schedule.end.hour)][0] = GroupSchedule.objects.get(id=schedule.id)
               e = schedule.end.hour - 1
            for i in range(s, e+1):
               schedule_list[str(i)][0] = GroupSchedule.objects.get(id=schedule.id)
               schedule_list[str(i)][1] = GroupSchedule.objects.get(id=schedule.id)
   comments=Comment.objects.filter(group=group)
   comment_list=list(comments)
   return render(request, 'groupCalendar.html',
   {'groupschedules':groupSchedules,'calendar' : cal, 'cur_month' : cur_month_url, 'prev_month' : prev_month_url, 'next_month' : next_month_url, 'groupId' : id,
   'schedule_list':schedule_list, 'date' : [today.year, str(today.month).zfill(2), str(day).zfill(2)],'comment_list':comment_list, 'members':members})

def get_date(request_day):
   if request_day:
      year, month = (int(x) for x in request_day.split('-'))
      return datetime.date(year, month, day=1)
   return datetime.datetime.today()

def prev_month(day):                                                          # 이전 달에 해당하는 URL 리턴
   first = day.replace(day=1)                                                 # first = today가 있는 달의 첫번째 날이 됨
   prev_month = first - datetime.timedelta(days=1)                            # prev_month = 첫 번째 날에서 하루를 뺌, 즉 저번 달 말일이 됨
   month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
   return month

def next_month(day):                                                          # 다음 달에 해당하는 URL 리턴
   days_in_month = calendar.monthrange(day.year, day.month)[1]
   last = day.replace(day=days_in_month)                                      # last = today가 있는 달의 마지막 날이 됨
   next_month = last + datetime.timedelta(days=1)                             # next_month = today에서 하루가 더 해진 날, 즉 다음 달 1일이 됨
   month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
   return month

def createGroupSchedule(request, id):
   newGroupSchedule = GroupSchedule()
   newGroupSchedule.group = Group.objects.get(pk=id)
   start_date = request.POST.get('start_date')
   start_hour = request.POST.get('start_hour')
   start_minute = request.POST.get('start_minute')
   startdatetime=str(start_date + ' ' + start_hour + ':' + start_minute+':00')
   newGroupSchedule.start = datetime.datetime.strptime(startdatetime,'%Y-%m-%d %H:%M:%S')
   end_date = request.POST.get('end_date')
   end_hour = request.POST.get('end_hour')
   end_minute = request.POST.get('end_minute')
   enddatetime=str(end_date + ' ' + end_hour + ':' + end_minute+':00')
   newGroupSchedule.end = datetime.datetime.strptime(enddatetime,'%Y-%m-%d %H:%M:%S')
   newGroupSchedule.title =  request.POST.get('title')
   newGroupSchedule.save()
   return redirect('groupCalendar_view',newGroupSchedule.group.id)

def addComment(request, id):
    comment=Comment()
    comment.writer=request.user
    #로그인 완성되면 수정 comment.writer=request.user
    comment.group = Group.objects.get(pk=id)
    comment.pub_date=timezone.datetime.now()
    comment.content=request.POST.get('content',False)
    comment.save()
    return redirect('groupCalendar_view',id)


def allowRegister(request, id):
   groupSchedule = GroupSchedule.objects.get(pk = id)
   newUserSchedule = Schedule()
   userid = request.session.get('user')  # 로그인세션
   newUserSchedule.user = CustomUser.objects.get(pk = userid)
   newUserSchedule.start =  groupSchedule.start
   newUserSchedule.end = groupSchedule.end
   newUserSchedule.title = groupSchedule.title
   newUserSchedule.save()
   return redirect('groupCalendar', groupSchedule.group_id)

def makeGroup(request):
   if request.method =='POST':
      inputfriendId = request.POST.get('input-friendId')
      allfriends=CustomUser.objects.all()
      allfriend_nickname=[]
      for friend in allfriends:
         allfriend_nickname.append(friend.nickname)
         if(friend.nickname==inputfriendId):
            if(friend in friend_list):
               messages.warning(request, "이미 추가한 친구 입니다.")
               return redirect('makeGroup')
            else:
               if(inputfriendId==request.user.nickname):
                  messages.warning(request, "본인")
                  return redirect('makeGroup')
               else:
                  friend_list.append(friend)
      if(inputfriendId not in allfriend_nickname):
         messages.warning(request, "존재하지 않는 이름입니다.")
         return redirect('makeGroup')
   return render(request,'makeGroup.html',{'friend_list':friend_list})

def sendInvitation(request):
   if(len(friend_list)>0):
      group=Group()
      group.name="안녕"
      group.save()
      usergroup=UserGroup()
      usergroup.user=request.user
      usergroup.group=group
      usergroup.allowed=2
      usergroup.save()
      for friend in friend_list:
         friend_usergroup=UserGroup()
         friend_usergroup.user=friend
         friend_usergroup.group=group
         friend_usergroup.allowed=1
         friend_usergroup.save()
         
      return redirect('groupCalendar_view', group.id)
   else:
      messages.warning(request, "친구를 초대해보세요")
      return redirect('makeGroup')