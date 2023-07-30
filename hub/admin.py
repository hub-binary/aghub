from django.contrib import admin 
from .models import *


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
admin.site.register(WeeklySchedule)


admin.site.site_header = "AGC Barnawa Admin"
admin.site.index_title = "AG Hub Admin"