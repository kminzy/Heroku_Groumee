from django.shortcuts import render, redirect,  get_object_or_404
from .models import User, Schedule, Group, GroupSchedule
import datetime
import calendar
from .calendar import Calendar
from django.utils.safestring import mark_safe


#Calendar: 한달 단위 모든 일정
#Schedule: 일정 하나 하나

# Create your views here.

def userCalendar_view(request):
   return render(request, 'userCalendar.html')

def getuserGroupList(request,userId):
   user = get_object_or_404(User, id=userId)
   userGroup_list=list(user.groups.all())  #userid를 받아와서 user가 속한 usergroup 부르기
   return render(request,'userGroupList.html',{'userGroup_list':userGroup_list})

def groupCalendar_view(request, id):            # 그룹 캘린더 보여주기
   today = get_date(request.GET.get('month'))

   prev_month_url = prev_month(today)
   next_month_url = next_month(today)
   
   # now = datetime.now()
   # cur_year = now.year        # 현재 연도
   # cur_month = now.month      # 현재 월

   group = Group.objects.get(id=id)
   cal = Calendar(today.year, today.month)
   cal = cal.formatmonth(withyear=True, group=group)
   cal = mark_safe(cal)

   return render(request, 'groupCalendar.html', {'calendar' : cal, 'prev_month' : prev_month_url, 'next_month' : next_month_url, 'groupId' : id})

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



def addgroupSchedule(request,userlist):  #list를 인자로 받아와도 되는지?

   groupschedulelist=[]
   for user in userlist:
      schedule=Schedule.objects.filter(user=user)
      groupschedulelist.append(schedule)
   return render(request, 'groupCalendar.html',{'groupschedule_list':groupschedulelist})


