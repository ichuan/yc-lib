from django.conf.urls.defaults import *

urlpatterns = patterns('ycdjbbs.bbs.views',
    # Example:
    # (r'^ycdjbbs/', include('ycdjbbs.foo.urls')),
    url(r'^$', 'post_list'),
    url(r'^post/new$', 'new_post'),
    url(r'^post/edit/(\d+)$', 'edit_post'),
    url(r'^post/del/(\d+)$', 'del_post'),
    url(r'^post/(\d+)$', 'view_post'),
    url(r'^reply/(\d+)$', 'new_reply'),
)
