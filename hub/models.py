from django.db import models
from os import urandom
from django.utils.timesince import timesince, timeuntil
from filebrowser.fields import FileBrowseUploadField
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
# from modelcluster.fields import ParentalKey
from django.forms import CheckboxSelectMultiple, SelectMultiple
# from wagtail.models import Page, Orderable
# from wagtail.fields import RichTextField, StreamField
# from wagtail.admin.panels import (
#     FieldPanel, MultiFieldPanel, InlinePanel,
#     PageChooserPanel, MultipleChooserPanel
#     )
# from wagtail.search import index


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
    UploadPath = 'sermons'
    public = models.BooleanField(default=True)
    cover_image = FileBrowseUploadField('Cover Image File', max_length=300, directory='images/covers/sermons/', blank=True, null=True)
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
    event_venue = models.CharField(max_length=200, blank=True, null=True, default="Church Premises")
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
    week = models.DurationField(null=True, blank=True, default=timedelta(weeks=1))
    schedule = models.ManyToManyField(ScheduleItem, blank=True)

    def save(self, *args, **kwargs):
        print("Saving...", self.week)
        # Convert the selected value to the appropriate duration
        if self.week == timedelta(days=1):
            self.week = timedelta(days=1)
            print("1 day")
        elif self.week == timedelta(weeks=1):
            self.week = timedelta(weeks=1)
            print("1 week")
        elif self.week == timedelta(weeks=2):
            self.week = timedelta(weeks=2)
            print("2 weeks")
        elif self.week == relativedelta(months=1):
            self.week = relativedelta(months=1)
            print("1 month")
        elif self.week == relativedelta(months=2):
            self.week = relativedelta(months=2)
            print("2 months")
        elif self.week == relativedelta(months=3):
            self.week = relativedelta(months=3)
            print("3 months")
        elif self.week == relativedelta(months=6):
            self.week = relativedelta(months=6)
            print("6 months")
        super().save(*args, **kwargs)



# from wagtail.search import index

# class BlogIndex(Page):
#     """
#     A BlogIndex page to display a list of blog posts.
#     """
    
#     body = RichTextField(blank=True)    
#     featured_blog_posts = models.ManyToManyField("BlogPage", blank=True, related_name='+')
#     # featured_posts = models.ForeignKey("BlogPage", null=True, blank=True, on_delete=models.SET_NULL)

#     content_panels = Page.content_panels + [
#         FieldPanel('title'),
#         FieldPanel('slug'),
#         FieldPanel('body', classname="full"),
#     ]

#     subpage_types = ['BlogPage']
#     template = 'hub/blog_index.html'
    
#     # from .models import BlogPage
#     promote_panels = Page.promote_panels + [
#         MultiFieldPanel([
#             # PageChooserPanel('featured_blog_posts', BlogPage),
#             FieldPanel('featured_blog_posts', widget=SelectMultiple),
#         ], heading="Featured Blog Posts"),

#     ]

#     def get_context(self, request, *args, **kwargs):
#         # Customize the context as needed to display a list of blog posts
#         context = super().get_context(request, *args, **kwargs)
#         children = context['page'].get_children().filter(live=True)
#         context['blogposts'] = children
        
#         # for post in children:
#         #     print("POST:", dir(post.blogpage.feed_image))
#         context['featured_posts'] = children
#         context['recent_posts'] = children
#         return context



# class BlogPage(Page):
#     parent = ParentalKey(BlogIndex, blank=True, null=True, on_delete=models.SET_NULL, related_name='featured_posts')
#     body = RichTextField()
#     date = models.DateField("Post date")
#     featured = models.BooleanField(default=False)
#     feed_image = models.ForeignKey(
#         'wagtailimages.Image',
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name='+'
#     )


#     # Search index configuration

#     search_fields = Page.search_fields + [
#         index.SearchField('body'),
#         index.FilterField('date'),
#     ]


#     # Editor panels configuration
#     content_panels = Page.content_panels + [
#         FieldPanel('date'),
#         FieldPanel('body'),
#         InlinePanel('related_links', heading="Related links", label="Related link"),
#     ]

#     promote_panels = [
#         MultiFieldPanel(Page.promote_panels, "Common page configuration"),
#         FieldPanel('feed_image'),
#         FieldPanel('featured'),
#     ]

#     # Parent page / subpage type rules
#     parent_page_types = ['hub.BlogIndex']
#     subpage_types = []

#     def get_context(self, request, *args, **kwargs):
#         # Customize the context as needed to display a list of blog posts
#         context = super().get_context(request, *args, **kwargs)
#         today = datetime.now()
#         posts = self.get_parent().get_children()
#         posts = posts.filter(live=True).exclude(id=self.id).order_by('-blogpage__date')[:5]
#         context['recent_posts'] = posts
        
#         # context['related_posts'] = children
#         return context


# class BlogPageRelatedLink(Orderable):
#     page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='related_links')
#     name = models.CharField(max_length=255)
#     url = models.URLField()

#     panels = [
#         FieldPanel('name'),
#         FieldPanel('url'),
#     ]





