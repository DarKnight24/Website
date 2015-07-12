from django.conf.urls import url,patterns
from institute import views

urlpatterns = patterns('',
	url(r'^$', views.home, name = 'home'),
    url(r'^institute/boardofgovernor$', views.boardofgovernors, name = 'board_of_governors'),
    url(r'^institute/(?P<rank>[\w\-]+)$', views.adminis_view, name = 'admin_view'),
    url(r'^notification/(?P<notif_title_slug>[\w\-]+)/$',views.notification,name = 'notification'),
	url(r'^notification/$',views.notification_all,name = 'index_notific'),
    url(r'^antiragging/$',views.antiragging,name = 'antiragging'),
    url(r'^rti/$', views.rti, name = 'rti'),
	)
