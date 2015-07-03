import random
from django.shortcuts import render, HttpResponse
from django.http import Http404
from django.db.models import Sum
from dept.models import *
from institute.models import Notification
from itertools import izip_longest
from collections import OrderedDict

# Create your views here.
context_dict = {}

def department(request, dept_code):
    try:
        dept = Department.objects.get(dept_code = dept_code)
        context_dict['Department'] = dept
        try:
            notific = Notification.objects.filter(notif_of=dept_code).order_by('date')[:10]
        except:
            notific = []
        context_dict['Notification'] = notific
        try:
            galler = Gallery.objects.filter(gallery_of = dept_code)
            try:
                img = Image.objects.filter(gallery_id = galler.gallery_id).order_by('-upload_date')[:10]
            except:
                img = []
            context_dict['Images'] = img
                
        except:
            pass
        html = dept_code+'/home.html'
    except:
        raise Http404

    return  render(request, html, context_dict)


def faculty(request,dept_code):
    try:
        dept = Department.objects.get(dept_code = dept_code)
        context_dict['Department'] = dept
    except:
        raise Http404
    try:
        faculties = Faculty.objects.filter(dept=dept_code)
        context_dict['Faculties'] = faculties

    except:
        raise Http404
    return render(request,'faculty.html',context_dict)
 


def student(request,dept_code):
    try:
        dept = Department.objects.get(dept_code = dept_code)
        context_dict['Department'] = dept
    except:
        raise Http404
    try:
        btech = Student.objects.filter(dept = dept_code, degree = 1).values('year_of_admission')
        idd = Student.objects.filter(dept = dept_code, degree = 2).values('year_of_admission')

        btech_years = list()
        idd_years = list()
        
        for i in btech: btech_years.append(i['year_of_admission'])
        for i in idd: idd_years.append(i['year_of_admission'])
        
        btech_years = sorted(list(OrderedDict.fromkeys(btech_years)),reverse=True)
        idd_years = sorted(list(OrderedDict.fromkeys(idd_years)),reverse=True)
        
        students_list_btech = list()
        counter = 0
        for i in btech_years:
            students_list_btech.append(Student.objects.filter(dept = dept_code, degree = 1, year_of_admission = btech_years[counter]).order_by('roll_no'))
            counter += 1

        students_list_idd = list()
        counter = 0 
        for i in idd_years: 
            students_list_idd.append(Student.objects.filter(dept = dept_code, degree = 2, year_of_admission = idd_years[counter]).order_by('roll_no'))
            counter += 1

        headings_btech  = [ "B.Tech Part - I",
                            "B.Tech Part - II",
                            "B.Tech Part - III",
                            "B.Tech Part - IV" ]
        headings_idd    = [ "IDD Part - I",
                            "IDD Part - II",
                            "IDD Part - III",
                            "IDD Part - IV",
                            "IDD Part - V" ]

        #Every value in each counter needs to be different.
        counter1 = [1,2,3,4]
        counter2 = [11,22,33,44,55]
        full_list_btech = izip_longest(  
                                counter1,
                                headings_btech,
                                students_list_btech  )
        full_list_idd   = izip_longest(  
                                counter2,
                                headings_idd,
                                students_list_idd  )
        context_dict['full_list_btech'] = full_list_btech
        context_dict['full_list_idd'] = full_list_idd

    except:
        raise Http404
    return render(request,'student.html',context_dict)


def phd(request, dept_code):
    try:
        dept = Department.objects.get(dept_code = dept_code)
        context_dict['Department'] = dept
    except:
        raise Http404
    try:
        phd_list = Phd.objects.filter(dept = dept_code)
        context_dict['Phd'] = phd_list
    except:
        raise Http404
    return render(request,'student.html',context_dict)


def staff(request, dept_code):
    try:
        dept = Department.objects.get(dept_code = dept_code)
        context_dict['Department'] = dept
    except:
        raise Http404
    try:
        staffs = Staff.objects.filter(dept = dept_code)
        context_dict['staff'] = staffs
    except:
        raise Http404
    return render(request,'staff.html',context_dict)


def visitor(request, dept_code):
    try:
        dept = Department.objects.get(dept_code = dept_code)
        context_dict['Department'] = dept
    except:
        raise Http404
    return render(request,'visitor.html',context_dict)

    
def alumni(request, dept_code):
    try:
        dept = Department.objects.get(dept_code = dept_code)
        context_dict['Department'] = dept
    except:
        raise Http404
    html = dept_code+'/alumni.html'
    return render(request,html,context_dict)

    
def dept_admission(request, dept_code):
    try:
        dept = Department.objects.get(dept_code = dept_code)
        context_dict['Department'] = dept
    except:
        raise Http404
    html = dept_code+'/admission.html'
    return render(request,html,context_dict)


def course(request, dept_code):
    try:
        dept = Department.objects.get(dept_code = dept_code)
        context_dict['Department'] = dept
    except:
        raise Http404
    try:
        theory_btech = list()
        practical_btech = list()
        btech_counter = [3,4,5,6,7,8]
        for i in btech_counter:
            theory_btech.append(Course.objects.filter(dept = dept_code, sem = i, b_tech = 1, type = 1).order_by('course_code'))

        for i in btech_counter:
            practical_btech.append(Course.objects.filter(dept = dept_code, sem = i, b_tech = 1, type = 2).order_by('course_code'))
    
        theory_idd = list()
        practical_idd = list()
        idd_counter = [3,4,5,6,7,8,9,10]
        for i in idd_counter:
            theory_idd.append(Course.objects.filter(dept = dept_code, sem = i, idd = 1, type = 1).order_by('course_code'))

        for i in idd_counter:
            practical_idd.append(Course.objects.filter(dept = dept_code, sem = i, idd = 1, type = 2).order_by('course_code'))
        
        #Total credits and contact hours of Semester.
        cred_total_btech_t = Course.objects.filter(dept = dept_code, b_tech = 1, type = 1).values('sem').annotate(sum = Sum('credits'))
        hrs_total_btech_t = Course.objects.filter(dept = dept_code, b_tech = 1, type = 1).values('sem').annotate(sum = Sum('contact_hours'))
        cred_total_btech_p = Course.objects.filter(dept = dept_code, b_tech = 1, type = 2).values('sem').annotate(sum = Sum('credits'))
        hrs_total_btech_p = Course.objects.filter(dept = dept_code, b_tech = 1, type = 2).values('sem').annotate(sum = Sum('contact_hours'))
        sem_cred_btech = Course.objects.filter(dept = dept_code, b_tech = 1).values('sem').annotate(sum = Sum('credits'))
        sem_hrs_btech = Course.objects.filter(dept = dept_code, b_tech = 1).values('sem').annotate(sum = Sum('contact_hours'))
        cred_total_idd_t = Course.objects.filter(dept = dept_code, idd = 1, type = 1).values('sem').annotate(sum = Sum('credits'))
        hrs_total_idd_t = Course.objects.filter(dept = dept_code, idd = 1, type = 1).values('sem').annotate(sum = Sum('contact_hours'))
        cred_total_idd_p = Course.objects.filter(dept = dept_code, idd = 1, type = 2).values('sem').annotate(sum = Sum('credits'))
        hrs_total_idd_p = Course.objects.filter(dept = dept_code, idd = 1, type = 2).values('sem').annotate(sum = Sum('contact_hours'))
        sem_cred_idd = Course.objects.filter(dept = dept_code, idd = 1).values('sem').annotate(sum = Sum('credits'))
        sem_hrs_idd = Course.objects.filter(dept = dept_code, idd = 1).values('sem').annotate(sum = Sum('contact_hours'))

        sum_cred_total_btech_t = list()
        sum_hrs_total_btech_t = list()
        sum_cred_total_idd_t = list()
        sum_hrs_total_idd_t = list()
        sum_cred_total_btech_p = list()
        sum_hrs_total_btech_p = list()
        sum_cred_total_idd_p = list()
        sum_hrs_total_idd_p = list()
        sum_sem_cred_btech = list()
        sum_sem_hrs_btech = list()
        sum_sem_cred_idd = list()
        sum_sem_hrs_idd = list()

        
        for i in cred_total_btech_t: sum_cred_total_btech_t.append(i['sum'])
        for i in hrs_total_btech_t: sum_hrs_total_btech_t.append(i['sum'])
        for i in cred_total_idd_t: sum_cred_total_idd_t.append(i['sum'])
        for i in hrs_total_idd_t: sum_hrs_total_idd_t.append(i['sum'])
        for i in cred_total_btech_p: sum_cred_total_btech_p.append(i['sum'])
        for i in hrs_total_btech_p: sum_hrs_total_btech_p.append(i['sum'])
        for i in cred_total_idd_p: sum_cred_total_idd_p.append(i['sum'])
        for i in hrs_total_idd_p: sum_hrs_total_idd_p.append(i['sum'])
        for i in sem_cred_btech: sum_sem_cred_btech.append(i['sum'])
        for i in sem_hrs_btech: sum_sem_hrs_btech.append(i['sum'])
        for i in sem_cred_idd: sum_sem_cred_idd.append(i['sum'])
        for i in sem_hrs_idd: sum_sem_hrs_idd.append(i['sum'])
        
        sem_title_btech = [ "Part - II : Semester III",
                            "Part - II  : Semester IV",
                            "Part - III : Semester V",
                            "Part - III : Semester VI",
                            "Part - IV : Semester VII",
                            "Part - IV : Semester VIII" ]
        sem_title_idd   = [ "Part - II : Semester III",
                            "Part - II : Semester IV",
                            "Part - III : Semester V",
                            "Part - III : Semester VI",
                            "Part - IV : Semester VII",
                            "Part - IV : Semester VIII",
                            "Part - V : Semester IX",
                            "Part - V : Semester X" ]

        #Every value in each counter needs to be different.
        counter1 = [1,2,3,4,5,6]
        counter2 = [11,22,33,44,55,66,77,88]

        btech_list      = izip_longest( 
                            counter1,
                            sem_title_btech,
                            theory_btech,
                            practical_btech,
                            sum_cred_total_btech_t,
                            sum_hrs_total_btech_t,
                            sum_cred_total_btech_p,
                            sum_hrs_total_btech_p,
                            sum_sem_cred_btech,
                            sum_sem_hrs_btech )
        idd_list        = izip_longest( 
                            counter2,
                            sem_title_idd,
                            theory_idd,
                            practical_idd,
                            sum_cred_total_idd_t,
                            sum_hrs_total_idd_t,
                            sum_cred_total_idd_p,
                            sum_hrs_total_idd_p,
                            sum_sem_cred_idd,
                            sum_sem_hrs_idd )

        context_dict['btech_list'] = btech_list
        context_dict['idd_list'] = idd_list

    except:
        raise Http404
    return render (request,'course.html', context_dict)


def research(request, dept_code):
    try:
        dept = Department.objects.get(dept_code = dept_code)
        context_dict['Department'] = dept
    except:
        raise Http404
    try:
        supervisors = PhdResearch.objects.filter(dept = dept_code).values('supervisor')

        sv_list = list()
        for i in supervisors: sv_list.append(i['supervisor'])
        sv_list = list(OrderedDict.fromkeys(sv_list))

        counter = list()
        num = "0"
        for i in sv_list:
            counter.append(num)
            num = str(int(num)+1)

        z = zip(sv_list,counter)
        names = list()
        for i,j in z:
            print i,j
            s = "sv"+j
            context_dict[s] = PhdResearch.objects.filter(dept = dept_code, supervisor = i)
            names.append(context_dict[s])

        full_list = izip_longest(sv_list, names)
        context_dict['full_list'] = full_list
    except:
        raise Http404      
    html = dept_code+'/research.html'  
    return render(request,html,context_dict)


def publication(request, dept_code):
    try:
        dept = Department.objects.get(dept_code = dept_code)
        context_dict['Department'] = dept
    except:
        raise Http404
    try:
        publications = 1
    except:
        raise Http404
    def RandomColor():
        r = lambda: random.randint(0,255)
        return ('#%02X%02X%02X' % (r(),r(),r()))
    context_dict['RandomColor'] = RandomColor()
    return render(request,'dept_publications.html',context_dict)


def project(request, dept_code):
    try:
        dept = Department.objects.get(dept_code = dept_code)
        context_dict['Department'] = dept
    except:
        raise Http404
    try:
        projects = Project.objects.filter(dept = dept_code)
        context_dict['Projects'] = projects
    except:
        raise Http404
    return render(request,'project.html',context_dict)


def seminar(request, dept_code):
    try:
        dept = Department.objects.get(dept_code = dept_code)
        context_dict['Department'] = dept
    except:
        raise Http404
    return render(request,'seminar.html',context_dict)


def talk(request, dept_code):
    try:
        dept = Department.objects.get(dept_code = dept_code)
        context_dict['Department'] = dept
    except:
        raise Http404
    return render(request,'talk.html',context_dict)


def equipment(request, dept_code):
    try:
        dept = Department.objects.get(dept_code = dept_code)
        context_dict['Department'] = dept
    except:
        raise Http404
    return render(request,'equipment.html',context_dict)


def lab(request, dept_code):
    try:
        dept = Department.objects.get(dept_code = dept_code)
        context_dict['Department'] = dept
    except:
        raise Http404
    return render(request,'lab.html',context_dict)


def placement(request, dept_code):
    try:
        dept = Department.objects.get(dept_code = dept_code)
        context_dict['Department'] = dept
    except:
        raise Http404
    html = dept_code+'/placement.html'
    return render(request,html,context_dict)


def contact(request, dept_code):
    try:
        dept = Department.objects.get(dept_code = dept_code)
        context_dict['Department'] = dept
    except:
        raise Http404
    return render(request,'contact.html',context_dict)


def notification_all(request, dept_code=None):
    context_dict['slug'] = None
    if dept_code:

        try:
            dept = Department.objects.get(dept_code = dept_code)
            context_dict['Department'] = dept
        except:
            raise Http404
        try:
            notification = Notification.objects.filter(notif_of=dept_code)
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

