from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text


@python_2_unicode_compatible
class UserProfile(models.Model):

    user = models.OneToOneField(User, verbose_name='user', related_name='profile', primary_key=True)
    roll_number = models.IntegerField(max_length=10, blank=False, null=False)
    year = models.IntegerField(max_length=1, blank=True, null=True)
    branch_code = models.IntegerField(max_length=2, blank=True, null=True)
    branch = models.CharField(max_length=3, blank=True, null=True)
    course = models.CharField(max_length=10, blank=True, null=True)
    avatar_url = models.ImageField("avatar_url", upload_to='profile_images', blank=True)
    dob = models.DateField(verbose_name="dob", blank=True, null=True)
    cv = models.FileField("resume", upload_to='resumes', blank=True)
    tenth = models.IntegerField(blank=True, null=True)
    twelfth = models.IntegerField(blank=True, null=True)
    graduation = models.IntegerField(blank=True, null=True)
    phone_no = models.IntegerField(max_length=10, blank=True, null=True)
    address = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return force_text(self.user.username)

    class Meta():
        db_table = 'user_profile'


class ProjectDetails(models.Model):

    title = models.CharField(max_length=100, null=False)
    body = models.TextField(null=False)
    report = models.FileField("Project_Report", upload_to='project_report', blank=True)
    user = models.ForeignKey(UserProfile, null=False, blank=False)

    def __str__(self):
        return force_text(self.title)