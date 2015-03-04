from django.db import models
from django.contrib.auth.models import User
# from spirit_user_profile.models import User
# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length = 15)
    def __unicode__(self):
        return self.name

class Link(models.Model):
    # number = models.IntegerField()
    name = models.CharField(max_length = 200, null=True)
    linl_type = models.CharField(max_length = 200,null=True)
    url_link = models.URLField()
    def __unicode__(self):
        return self.url_link

class Step(models.Model):
    number = models.IntegerField()
    links = models.ManyToManyField(Link,blank=True)
    short_description = models.CharField(max_length = 250,blank = 'True')
    long_description = models.TextField(blank = 'True')
    resources = models.TextField(blank = 'True')
    time = models.CharField(max_length=50)
    forum = models.URLField(null=True,blank=True)
    def __unicode__(self):
        return self.number

class Path(models.Model):
    name = models.CharField(max_length = 100,verbose_name = 'Event Name' ,unique = True)
    steps = models.ManyToManyField(Step,blank=True)
    tag = models.ManyToManyField(Tag,blank=True)
    short_description = models.CharField(max_length = 250,blank = 'True')
    long_description = models.TextField(blank = 'True',null=True)
    # attachments=models.FileField(blank=True,upload_to="attachments")
    author = models.ForeignKey(User, null = True , blank = True,verbose_name = 'author')
    online = models.BooleanField(verbose_name = 'Enable online registration')
    no_registrations = models.IntegerField(null = True,blank = True)
    upvotes = models.IntegerField( null = True, blank = True)
    forum = models.URLField(null=True,blank=True)
    prereq = models.TextField(blank = 'True',null=True)
    outcomes = models.TextField(blank = 'True',null=True)
    faq = models.TextField(blank = 'True',null=True)
    img=models.ImageField(blank=True, upload_to="imageuploads", null=True)
    # thumb=models.ImageField(blank=True, upload_to="imageuploads")
    time = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name
class PathStudent(models.Model):
    course = models.ForeignKey(Path)
    step = models.IntegerField()
    def __unicode__(self):
        return str(self.course)
class UserInfo(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    user = models.ForeignKey(User, unique=True, blank=True,null=True)
    bio = models.CharField(max_length = 350,blank = 'True')
    website = models.URLField()
    img=models.ImageField(blank=True, upload_to="imageuploads")
    courses_student = models.ManyToManyField(PathStudent,blank=True)
    def __unicode__(self):
        return str(self.name)



