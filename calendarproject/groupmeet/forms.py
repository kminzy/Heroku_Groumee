from django import forms
from .models import Schedule
from django.core.exceptions import ValidationError

class UserScheduleCreationForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('start', 'end', 'title')
        widgets = {'start' : forms.DateTimeInput(attrs={'type' : 'datetime-local'}),
                    'end' : forms.DateTimeInput(attrs={'type' : 'datetime-local'})}
        error_messages = {
            'start': {
                'required': "일정 시작 시간을 입력해주세요",
            },

            'end' : {
                'required': "일정 종료 시간을 입력해주세요",
            },

            'title' : {
                'required' : "일정 이름을 입력해주세요",
            },
        }

    def clean_end(self):
        start = self.cleaned_data.get('start')
        end = self.cleaned_data.get('end')

        if start >= end:
            raise ValidationError("일정이 끝나는 시간이 시작시간보다 이후여야 합니다")
        return end