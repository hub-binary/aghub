from django.urls import path
from .views import (
    home_view,
    sermons_view,
    weekly_schedule_view,
    events_view,
    contact_view,
    sermon_download_view
)

app_name = 'hub'

urlpatterns = [
    path('contact/', contact_view, name='contact'),
    path('sermons/', sermons_view, name='sermons'),
    path('sermons/<slug>/', sermon_download_view, name='sermon-download'),
    path('events/', events_view, name='events'),
    path('week/', weekly_schedule_view, name='week'),
    path('', home_view, name='home'),
]
