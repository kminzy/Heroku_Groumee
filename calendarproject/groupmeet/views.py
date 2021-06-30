from django.shortcuts import render
import calendar
from calendar import HTMLCalendar

# Create your views here.

def usercalendar(request):
    return render(request, 'userCalendar.html')