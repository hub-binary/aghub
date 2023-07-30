from django.db import models
from os import urandom
from django.utils.timesince import timesince, timeuntil
from filebrowser.fields import FileBrowseUploadField


def make_random(char_length=4):
    char = urandom(char_length).hex()
    return char

def slugify(character:str) -> str:
    slug = character.replace(' ', '-').replace('.', '').replace('\'', '').lower()
    return slug




# Create your models here.
class MediaFile(models.Model):
    UploadPath = ''
    FileField = FileBrowseUploadField
    file_id = models.CharField(max_length=10, default=make_random)
    date_time_created = models.DateTimeField(auto_created=True, auto_now=True)
    file_object = FileField('File', max_length=300, directory=UploadPath, blank=True, null=True)
    public = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Sermon(MediaFile):
    public = models.BooleanField(default=True)
    cover_image = FileBrowseUploadField('File', max_length=300, directory='images/covers/sermons/', blank=True, null=True)
    title = models.CharField(name='sermon_title', max_length=300)
    speaker = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(name="url_title", blank=True)
    date_released = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.url_title:
            self.url_title = slugify(self.sermon_title)
        return super().save(args, kwargs)

    def __str__(self) -> str:
        return self.sermon_title
        

class Event(MediaFile):
    UploadPath = 'files/events/flyers'
    file_object = models.FileField('event_flyer', upload_to=UploadPath, blank=True, null=True)
    event_name = models.CharField(max_length=300)
    event_start_date = models.DateField()
    event_stop_date = models.DateField(blank=True, null=True)
    event_description = models.TextField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    event_sermons = models.ManyToManyField(Sermon, blank=True, related_name='related_sermons')

    def __str__(self) -> str:
        return self.event_name


class Announcement(models.Model):
    title = models.CharField(name='short_description', max_length=300)
    details = models.TextField(blank=True, null=True)
    date_created =  models.DateTimeField(auto_created=True, auto_now=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title


class ScheduleItem(models.Model):
    weekday = models.DateField()
    time = models.TimeField()
    description = models.CharField(max_length=500)
    more_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.description


class WeeklySchedule(models.Model):
    week_end = models.DateField()
    schedule = models.ManyToManyField(ScheduleItem, blank=True)

    def __str__(self):
        return f'{self.week_end}'