from django.conf.urls import url,patterns
from dept import views

urlpatterns = patterns('',
    url(r'^department/(?P<dept_code>[\w\-]+)/$', views.department, name='dept_home'),
	url(r'^department/(?P<dept_code>[\w\-]+)/people/faculty/$',views.faculty,name ='faculty'),
	url(r'^department/(?P<dept_code>[\w\-]+)/people/student/$',views.student,name='student'),
	url(r'^department/(?P<dept_code>[\w\-]+)/people/staff/$',views.staff,name='staff'),
	url(r'^department/(?P<dept_code>[\w\-]+)/people/visitor/$',views.visitor,name='visitor'),
	url(r'^department/(?P<dept_code>[\w\-]+)/people/alumni/$',views.alumni,name='alumni'),
	url(r'^department/(?P<dept_code>[\w\-]+)/admission/$',views.dept_admission,name='dept_admission'),
	url(r'^department/(?P<dept_code>[\w\-]+)/course/$',views.course,name='course'),
	url(r'^department/(?P<dept_code>[\w\-]+)/course/btech/$',views.course,name='btech'),
	url(r'^department/(?P<dept_code>[\w\-]+)/course/mtech_idd/$',views.course,name='mtech_idd'),
	url(r'^department/(?P<dept_code>[\w\-]+)/course/phd/$',views.course,name='phd'),
	url(r'^department/(?P<dept_code>[\w\-]+)/research/$',views.research,name='research'),
	url(r'^department/(?P<dept_code>[\w\-]+)/facilities/lab/$',views.lab,name='lab'),
	url(r'^department/(?P<dept_code>[\w\-]+)/facilities/equipment/$',views.equipment,name='equipment'),
	url(r'^department/(?P<dept_code>[\w\-]+)/activities/publications/$',views.publication,name='publication'),
	url(r'^department/(?P<dept_code>[\w\-]+)/activities/projects/$',views.project,name='project'),
	url(r'^department/(?P<dept_code>[\w\-]+)/activities/seminars-and-conferences/$',views.seminar,name='seminar'),
	url(r'^department/(?P<dept_code>[\w\-]+)/activities/tech-talks/$',views.talk,name='talk'),
	url(r'^department/(?P<dept_code>[\w\-]+)/placement/$',views.placement,name='placement'),
	url(r'^department/(?P<dept_code>[\w\-]+)/contact/$',views.contact,name='contact'),
	url(r'^department/(?P<dept_code>[\w\-]+)/notification/$',views.notification_all, name = 'dept_notific'),
    url(r'^department/(?P<dept_code>[\w\-]+)/notification/(?P<notif_title_slug>[\w\-]+)/$',views.notification, name = 'dept_notific_view'),
    url(r'^/static/js/ViewerJS/$',views.viewerjs,name='viewerjs'),
	
	)

