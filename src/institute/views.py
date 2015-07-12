from django.shortcuts import render, HttpResponse
from django.http import Http404
from django.db.models import Sum
from institute.models import *
from dept.models import *
from itertools import izip_longest
from collections import OrderedDict

# Create your views here.
context_dict = {}


def home(request):
    try:
        semis = Seminars_conf.objects.order_by('date')[:5]
    except:
        semis = []
    context_dict['Seminar'] = semis 
    
    try:
        notific = Notification.objects.filter(notif_of='Institute').order_by('date')[:10]
        try:
            context_dict['head'] = notific[0]
            context_dict['Notifications'] = notific[1:]
        except:
            pass
    except:
        context_dict['Notifications'] = []
    try:
        galler = Gallery.objects.filter(gallery_of = 'Institute')
        try:
            img = Image.objects.filter( gallery_id = galler.gallery_id ).order_by('-upload_date')[:10]
        except:
            img = {}
        context_dict['Images'] = img
    except:
        pass 
    return render(request,'index.html',context_dict)



def boardofgovernors(request):  
    try:
        board = BoardOfGovernor.objects.all()
        context_dict['Board_mem'] = board
        rank_title = ["Chairman",
                      "Director(Ex-officio)Member",
                      "Members",
                      "Secretary",
                      ]
        counter = [1,2,3,4,5,6,7,8,9,0]
        full_list = zip(counter,rank_title)
        context_dict['full_list'] = full_list
    except:
        raise Http404
    return render(request,'bog.html',context_dict)


def notification_all(request, dept_code=None):
    context_dict['slug'] = None
    if dept_code:
        dept_code1 = dept_code[:2].upper()
        try:
            dept = Department.objects.get(dept_code = dept_code1)
            context_dict['Department'] = dept
        except:
            raise Http404
        try:
            notification = Notification.objects.filter(notif_of=dept_code1)
            context_dict['notifications'] = notification
        except:
            raise Http404
        return render(request,'dept_notification.html',context_dict)
    else:
        try:
            notification = Notification.objects.filter(notif_of = "Institute")
            context_dict['notifications'] = notification
        except:
            raise Http404
        context_dict['slug'] = None
        return render(request,'notification.html',context_dict)
 

def notification(request,notif_title_slug, dept_code=None):
    context_dict['slug'] = notif_title_slug
    try:
        notification = Notification.objects.filter(slug=notif_title_slug)
        context_dict['notification'] = notification
    except:
        raise Http404
    if dept_code:
        return render(request,'dept_notification.html',context_dict)
    else:
        return render(request,'notification.html',context_dict)


def administration(request):
    try:
        admin = AdminOffical.objects.get().order_by(rank_id)
        context_dict['adminis'] = admin
    except:
        raise Http404
    return render(request,'administration.html',context_dict)

def adminis_view(request,rank):
    try:
        members = AdminOfficials.objects.filter(rank_name=rank)
        context_dict['official'] = members
    except:
        raise Http404
    return render(request,'administration_view.html',context_dict) 


def committee(request):
    try:
        commit = Committee.objects.get().order_by(comm_id)
        context_dict['committees']= commit
    except:
        return HttpResponse("Failed to retrieve data .")
    return render(request, 'committee.html',context_dict)


def committee_view(request):
    try:
        c_view = CommDetail.object.filter(comm_id = c_id )  
        context_dict['committs'] = c_view
    except:
        raise Http404
    return render(request, 'com_view.html',context_dict)


def antiragging(request):
    return render(request,'antiragging.html')


def gallery(request):
    return render(request,'gallery.html')

def rti(request):
    return render(request, 'rti.html')


