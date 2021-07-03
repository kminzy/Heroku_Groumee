from calendar import HTMLCalendar
from .models import Schedule, GroupSchedule

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, firstweekday=6):
        self.year = year
        self.month = month
        super(Calendar, self).__init__(firstweekday)

    def formatmonth(self, withyear=True, group=None):
        cal = f'<table class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'       # 영어로 몇 월인지, 몇 년도인지에 대한 문자열
        cal += '<tr><th colspan="2"><p onclick="go_prev_month();">저번달</p></th>' + f'<th colspan="3" class="month-number">{self.month}</th>' + '<th colspan="2"><p onclick="go_next_month();">다음달</p></th></tr>\n'
        cal += '<tr class="weekheader"><th class="sun">일</th><th class="mon">월</th><th class="tue">화</th><th class="wed">수</th><th class="thu">목</th><th class="fri">금</th><th class="sat">토</th></tr>\n' 
        # cal += f'{self.formatweekheader()}\n'                                              # 일 ~ 토 문자열 추가
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, group)}\n'
        return cal + '</table>'

    def formatweek(self, theweek, group):
        week = ''
        for d, weekday in theweek:              # d : 몇일인지(5일, 15일..) weekday : 요일(0=sun, 6=sat)
            week += self.formatday(d, group)
        return f'<tr> {week} </tr>'

    def formatday(self, day, group):
        # schedules_per_day = schedules.filter(start__day=day) # 어떤 년도 어떤 달에 있는 스케줄 중에서 특정 '날'에 있는 스케줄만 필터링 -> 그 날 있는 스케줄들을 필터링한다
        # d = ''
        # for schedule in schedules_per_day:
        #     d += f'<li> {schedule.get_html_url} </li>'
        group_schedules = GroupSchedule.objects.filter(group=group, start__year=self.year, start__month=self.month, start__day=day) # 이 그룹의 그룹스케줄 중 이 날의 스케줄만 담음
        all_members_schedules = []            # 그룹의 모든 구성원들의 개인스케줄들 중에서, 이 날에 있는 스케줄들만 담을 리스트
        for member in group.members.all():
            all_members_schedules += Schedule.objects.filter(user=member.userId, start__year=self.year, start__month=self.month, start__day=day)
        if day != 0:
            if all_members_schedules or group_schedules:      # 그 날에 어떠한 스케줄(그룹스케줄이던 개인스케줄이던)이라도 있으면
                return f"<td class='date is_schedule' onclick='view_day_schedule(this);'>" + f"{day}</td>"
            else:                                             # 그 날에 아무 스케줄도 없으면
                return f"<td class='date is_not_schedule' onclick='view_day_schedule(this);'>{day}</td>"
        return '<td></td>'

