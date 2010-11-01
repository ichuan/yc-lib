from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to
from ycdjbbs.views import current_datetime

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    url(r'^$', redirect_to, {'url': '/bbs'}),
    url(r'^bbs/', include('ycdjbbs.bbs.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/register/$', 'ycdjbbs.bbs.views.register'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^accounts/profile/$', redirect_to, {'url': '/bbs'}),
)
