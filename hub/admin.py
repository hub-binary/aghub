from django.contrib import admin
from django import forms
from datetime import timedelta
from .models import *
from dateutil.relativedelta import relativedelta


class WeeklyScheduleAdminForm(forms.ModelForm):
    class Meta:
        fields = ['week', 'schedule']
        model = WeeklySchedule
        widgets = {
            'week': forms.Select(choices=[
                (1, '1 day'),
                (7, '1 week'),
                (14, '2 weeks'),
                (30, '1 month'),
                (7 * 4, '4 weeks'),
                (60, '2 months'),
                (7 * 10, '10 weeks'),
                (90, '3 months'),
                (180, '6 months'),
                (60, '2 months'),
                # Add more choices as needed
            ]),
        }

    # def clean_week(self):
    #     value = self.cleaned_data['week']
    #     if value == 1:
    #         return timedelta(days=1)
    #     elif value == 7:
    #         return timedelta(weeks=1)
    #     elif value == 14:
    #         return timedelta(weeks=2)
    #     elif value == 30:
    #         return relativedelta(months=1)
    #     elif value == 60:
    #         return relativedelta(months=2)
    #     elif value == 90:
    #         return relativedelta(months=3)
    #     elif value == 180:
    #         return relativedelta(months=6)
    #     else:
    #         return None



class ScheduleAdmin(admin.ModelAdmin):
    model = WeeklySchedule
    form = WeeklyScheduleAdminForm

    def save_model(self, request, obj, form, change):
        # Convert the selected value to the appropriate duration
        if form.cleaned_data['week'] == 1:
            obj.week = timedelta(days=1)
        elif form.cleaned_data['week'] == 7:
            obj.week = timedelta(weeks=1)
        elif form.cleaned_data['week'] == 14:
            obj.week = timedelta(weeks=2)
        elif form.cleaned_data['week'] == 30:
            obj.week = relativedelta(months=1)
        elif form.cleaned_data['week'] == 60:
            obj.week = relativedelta(months=2)
        elif form.cleaned_data['week'] == 90:
            obj.week = relativedelta(months=3)
        elif form.cleaned_data['week'] == 180:
            obj.week = relativedelta(months=6)
        else:
            print("Nothing Here..")
            obj.week = None
        super().save_model(request, obj, form, change)




class SermonAdmin(admin.ModelAdmin):
    model = Sermon

    list_display = [
        'sermon_title',
        'speaker',
    ]
    list_display_links = ['sermon_title', 'speaker', ]




# Register your models here.
admin.site.register(Announcement)
admin.site.register(Event)
admin.site.register(Sermon, SermonAdmin)
admin.site.register(ScheduleItem)
# admin.site.register(BlogPage)
# admin.site.register(BlogPageRelatedLink)
admin.site.register(WeeklySchedule, ScheduleAdmin)


admin.site.site_header = "AGC Barnawa Admin"
admin.site.index_title = "AG Hub Admin"