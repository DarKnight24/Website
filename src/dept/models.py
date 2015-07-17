import os
from django.db import models
from django.core.validators import RegexValidator, validate_email
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_unicode
from django.template.defaultfilters import slugify

#media root dirs.
MEDIA_ROOT_IMAGES = 'images/'
MEDIA_ROOT_GALLERY = 'gallery/'
MEDIA_ROOT_DOCUMENTS = 'documents/'


#Function for saving images/docs in dynamic path. 
def __get_path_faculty__(instance, filename):
    getDept = instance.dept.dept_code
    upload_dir = os.path.join(MEDIA_ROOT_IMAGES,getDept,'Faculty')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join(upload_dir, filename)

def __get_path_committees__(instance, filename):
    upload_dir = os.path.join(MEDIA_ROOT_DOCUMENTS,'Committees')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join(upload_dir, filename)

# Create your models here.

#validators 
alphanum = RegexValidator(r'^[0-9 a-z A-Z]*$','Only Alphanumeric values are allowed')
num = RegexValidator(r'^[0-9]*$','Only Integer values are allowed')
tenDigitContact = RegexValidator(r'^\d{10,10}$','Enter a Valid 10 digit number.', 'Invalid number')
emailValidation = RegexValidator(r'^[0-9_ a-z A-Z \-\.]+(@iitbhu\.ac\.in|@itbhu\.ac\.in)*$')


class Department(models.Model):
    dept_code = models.CharField(unique=True, max_length = 2, primary_key = True, blank = False,
                                 verbose_name="Department Code")
    dept_name = models.CharField(max_length = 50, blank=False, null=True, verbose_name="Department Name")
    contact1 = models.IntegerField(null = False, blank = False, validators=[tenDigitContact])
    contact2 = models.IntegerField(null = True, blank = True, validators=[tenDigitContact])
    b_tech = models.BooleanField(default=True, verbose_name="B.Tech")
    idd = models.BooleanField(default=True, verbose_name="IDD")
    m_tech = models.BooleanField(default=True, verbose_name="M.Tech")
    ph_d = models.BooleanField(default=True, verbose_name="PhD")

    def __unicode__(self):
        return smart_unicode(self.dept_code)+' : '+smart_unicode(self.dept_name)


class Faculty(models.Model):
    name = models.CharField(max_length = 50, blank = False)
    dept = models.ForeignKey(Department, blank=False, verbose_name="Department")
    photo = models.ImageField(upload_to = __get_path_faculty__, default = 'null')
    designation = models.CharField(max_length = 50, null = True, blank = True)
    qualification = models.CharField(max_length = 100, null = True, blank = True)
    area_of_interest = models.CharField(max_length = 100, null = True, blank = True)
    contact_off = models.IntegerField(null = True, blank = True, validators=[tenDigitContact],
                                      verbose_name="Contact office")
    contact_res = models.IntegerField(null = True, blank = True, validators=[tenDigitContact],
                                      verbose_name="Contact residence")
    contact_other = models.IntegerField(null = True, blank = True, validators=[tenDigitContact])
    email_off = models.EmailField(unique = True, null = False, blank = False, validators = [emailValidation],
                    error_messages = {'invalid':'Enter your Official Email-ID.'}, verbose_name="E-mail official")
    email_other = models.EmailField(unique = True,null = True, blank =True, default = None)
    #Available/Out of Station/On Leave
    status = models.CharField(max_length = 10, null = True, blank = True)
    faculty_id = models.CharField(unique=True, max_length =100, primary_key = True, editable = False)

    def save(self, *args, **kwargs):
        if not self.faculty_id:
            self.faculty_id = self.email_off.split('@')[0]
        super(Faculty,self).save(*args,**kwargs)
        #returns a none value for an empty string if the email field is left blank.
        if self.email_other == "":
            self.email_other = None
        super(Faculty,self).save(*args, **kwargs)

    def __unicode__(self):
        return smart_unicode(self.name)+' : '+smart_unicode(self.email_off)+' : '+smart_unicode(self.faculty_id)


class Student(models.Model):
    DEGREE = {
            (1,'B.Tech'),
            (2,'IDD'),
            (3,'M.Tech'), 
    }
    roll_no = models.CharField(unique = True, max_length = 20, primary_key = True, blank = False, validators=[alphanum])
    name = models.CharField(max_length = 50, null = False, blank = False)
    year_of_admission = models.PositiveSmallIntegerField(null = False, blank = False, default = 0, editable = False)
    degree = models.IntegerField(choices = DEGREE, default = 1)
    email = models.EmailField(unique = True, null = False, blank = False, validators = [emailValidation],
                              error_messages = {'invalid':'Enter your Official Email-ID.'})
    dept = models.ForeignKey(Department, verbose_name="Department")

    def save(self,*args,**kwargs):
        #extract year from email.
        self.year_of_admission = int((self.email.split('@')[0])[-2:])
        super(Student,self).save(*args,**kwargs)
    def __unicode__(self):
        return smart_unicode(self.roll_no)+' : '+smart_unicode(self.name)


class Phd(models.Model):
    name = models.CharField(max_length = 50, null = False, blank = False)    
    dept = models.ForeignKey(Department, verbose_name="Department")
    supervisor = models.CharField(max_length = 50, null = True, blank = True)
    co_supervisor = models.CharField(max_length = 50, null = True, blank = True)


class PhdResearch(models.Model):
    name = models.CharField(max_length = 50, null = False, blank = False)    
    dept = models.ForeignKey(Department, verbose_name="Department")
    supervisor = models.CharField(max_length = 50, null = True, blank = True)
    topic = models.CharField(max_length = 200, null = False, blank = False)    
    status = models.CharField(max_length = 50, null = False, blank = False)    


class Staff(models.Model):
    name = models.CharField(max_length = 50, null = False, blank = False)
    dept = models.ForeignKey(Department, null = False, blank = False, verbose_name="Department")
    designation = models.CharField(max_length = 50, null = False, blank = False)
    email = models.EmailField(null = True, blank = True)

    def __unicode__(self):
        return smart_unicode(self.name)+' : '+smart_unicode(self.email)


class Committee(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    comm_id = models.IntegerField(null = False, blank = False, verbose_name="committee ID")
    short = models.CharField(max_length=10, unique=True, blank=False, null=False, verbose_name="Short Form")
    notif_no = models.CharField(max_length = 100, null = True, blank = True, verbose_name="Notification number")
    dated = models.CharField(max_length = 100, null = True, blank = True)
    comm_doc = models.FileField(upload_to = __get_path_committees__, default = 'null', verbose_name="Notification Document")
    comm_img = models.ImageField(upload_to = __get_path_committees__, default = 'null', verbose_name="Notification Image")
    description = models.CharField(max_length=250, blank=True, null=True)

    def __unicode__(self):
        return smart_unicode(self.short) + ' : ' + smart_unicode(self.name)


class Post(models.Model):
    PEOPLE = {
            ('1','Faculty'),
            ('2','Student'),
            ('3','Staff'),
            ('4','Others'),
    }
    name = models.CharField(max_length=50)
    group = models.ForeignKey(Committee)
    post_hold_by = models.CharField(max_length=5, choices=PEOPLE)

    def __unicode__(self):
        return smart_unicode(self.name) + " : " + smart_unicode(self.group)


class StudentsPost(models.Model):
    post = models.ForeignKey(Post, limit_choices_to={'post_hold_by': '2'})
    roll_no = models.CharField(max_length = 20, blank = False, validators=[alphanum])


class FacultiesPost(models.Model):
    post = models.ForeignKey(Post, limit_choices_to={'post_hold_by': '1'})
    dept = models.ForeignKey(Department, verbose_name="Department")
    faculty = models.ForeignKey(Faculty)


class StaffsPost(models.Model):
    post = models.ForeignKey(Post, limit_choices_to={'post_hold_by': '3'})
    employee_id = models.CharField(max_length = 20, blank = False, validators=[alphanum])


class Course(models.Model):
    COURSE_TYPE = {
        (1,'Theory'),
        (2,'Practical'),
    }
    course_id = models.IntegerField(unique = True, primary_key = True)
    sem = models.IntegerField()
    course_code = models.CharField(max_length = 10, null = False, blank = False, default = 'null')
    course_name = models.CharField(max_length = 50, null = False, blank = False, default = 'null')
    credits = models.IntegerField(default = 0)
    contact_hours = models.IntegerField(default = 0)
    #Theory/Practical
    type = models.IntegerField(choices = COURSE_TYPE, default = 1)
    #Value = 1 for the appropriate degree
    b_tech = models.BooleanField(default=True)
    idd = models.BooleanField(default=True)
    m_tech = models.BooleanField(default=True)
    ph_d = models.BooleanField(default=True)
    dept = models.CharField(max_length = 3, null = False, blank = False)
    course_offered_by = models.CharField(max_length = 3, null = False, blank = False)

    def __unicode__(self):
        return smart_unicode(self.course_id)+' : '+smart_unicode(self.course_name)


class HeadOfDepartments(models.Model):
    dept = models.ForeignKey(Department , blank=False)
    name = models.ForeignKey(Faculty)
    
    def __unicode__(self):
        return smart_unicode(self.dept)


class Project(models.Model):
    UNITS = {
                ('Thousand','Thousand'),
                ('Lakhs','Lakhs'),
                ('Millions','Millions'),
                ('Crores','Crores'),
            }
    dept = models.ForeignKey(Department, blank=False)
    year = models.CharField(max_length = 30, null = True, blank = True)
    project = models.CharField(max_length = 100, null = False, blank = False)
    sponsor = models.CharField(max_length = 50, null = False, blank = False)
    amount = models.FloatField(default = 0.0)
    units = models.CharField(choices = UNITS, max_length = 15, null = False, blank = False)
    #Person who undertook the project
    investigator = models.CharField(max_length = 50, null = False, blank = False)

    def __unicode__(self):
        return smart_unicode(self.project)
