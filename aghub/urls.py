from django.urls import include, path, re_path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from filebrowser.sites import site
from django.core.files.storage import DefaultStorage
from filebrowser.sites import FileBrowserSite

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls


# Default FileBrowser site
site = FileBrowserSite(name='filebrowser', storage=DefaultStorage())
site.directory = ''

urlpatterns = [
    re_path('^hubmin/filebrowser/', site.urls),
    path('hubmin/', admin.site.urls),
    path('grappelli/', include('grappelli.urls')),
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    re_path('^blog/', include(wagtail_urls)),
    path('', include('hub.urls', namespace='public')),
] 

if settings.DEBUG:
    urlpatterns += static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)