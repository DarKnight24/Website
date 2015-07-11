from django.contrib import admin
# Register your models here.
from institute.models import *
from dept.models import *


# Create your models here.

class instituteAdmin(admin.ModelAdmin):
    class Meta:
        model = Department
        model = Faculty
        model = Student
        model = Staff
        model = Notification
        model = Course
        model = Gallery
        model = Image
        model = SeminarsConf
        model = Event
        model = Tender
        #model = Committee
        model = CommDetail
        model = AdminOfficial
        model = BoardOfGovernor
        #model = HostelAdmin
        model = RankList
        #model = History
        model = TenderDoc
        model = PhdResearch
        model = Phd
        model = Project

class HeadOfDepartmentAdmin(admin.ModelAdmin):
    model = Faculty
    list_filter = ("")


class NotificationAdmin(admin.ModelAdmin):  
    prepopulated_fields = {'slug':('title',)}
    list_filter = ['notif_of']
    #pass


class DepartmentHomepage(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ('dept_code', 'dept_name')}),
        ('Contact Details',     {'fields': ('contact1', 'contact2')}),
        ('Courses Offered',      {'fields': (('b_tech', 'idd', 'm_tech', 'ph_d'),)}),
    ]


class FacultyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ('dept', )}),
        ('Personal Detail', {'fields': (('name', 'photo'), ('designation',), ('qualification', 'area_of_interest'),)}),
        ('Contact Details', {'fields': (('contact_off', 'contact_res', 'contact_other'),
                                          ('email_off', 'email_other'),)}),
        (None,              {'fields': ('status',)})
    ]
    list_filter = ['dept']

class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Course detail',   {'fields': (('course_id','course_code'), 'sem', 'course_name', ('credits', 'contact_hours'),
                            'type', ('b_tech', 'idd', 'm_tech', 'ph_d'), ('dept', 'course_offered_by'))})
    ]


class DepartmentFilter(admin.ModelAdmin):
    list_filter = ['dept']

admin.site.register(Department, DepartmentHomepage)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Student)
admin.site.register(Staff, DepartmentFilter)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Project, DepartmentFilter)
admin.site.register(Gallery, instituteAdmin)
admin.site.register(Image, instituteAdmin)
admin.site.register(SeminarsConf, instituteAdmin)
admin.site.register(Event, instituteAdmin)
admin.site.register(Tender, instituteAdmin)
#admin.site.register(Committee, instituteAdmin)
admin.site.register(Groups, instituteAdmin)
admin.site.register(Post, instituteAdmin)
admin.site.register(StudentsPost, instituteAdmin)
admin.site.register(FacultiesPost, instituteAdmin)
admin.site.register(StaffsPost, instituteAdmin)
admin.site.register(CommDetail, instituteAdmin)
admin.site.register(AdminOfficial, instituteAdmin)
admin.site.register(BoardOfGovernor, instituteAdmin)
#admin.site.register(HostelAdmin, instituteAdmin)
admin.site.register(RankList, instituteAdmin)
#admin.site.register(History, instituteAdmin)
admin.site.register(TenderDoc, instituteAdmin)
admin.site.register(Security,instituteAdmin)
admin.site.register(HeadOfDepartments,instituteAdmin)
admin.site.register(RightToInformation,instituteAdmin)
admin.site.register(Calendar,instituteAdmin)
admin.site.register(Circulars,instituteAdmin)
#admin.site.register(Wmes,instituteAdmin)
admin.site.register(NewsBoard, instituteAdmin)
admin.site.register(PhdResearch, DepartmentFilter)
admin.site.register(Phd, DepartmentFilter)

