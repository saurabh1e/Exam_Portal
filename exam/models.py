from django.db import models
from user.models import UserProfile
from Exam_Portal.settings import SECRET_KEY
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text
from datetime import datetime

class Test(models.Model):
    name = models.CharField(max_length=50, unique=True)
    branch_code = models.IntegerField(max_length=2, blank=False, null=False)
    s_id = models.CharField(max_length=50, default=0, blank=True, null=True)
    time = models.IntegerField(max_length=3, blank=False, null=False)
    postive = models.IntegerField(max_length=1, blank=False, null=False)
    negative = models.IntegerField(max_length=1, blank=False, null=False)

    # def __init__(self, name, branch_code, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.name = name
    #     self.branch_code = branch_code
    #     print(name)
    def save(self, *args, **kwargs):
        from itsdangerous import URLSafeSerializer
        s = URLSafeSerializer(SECRET_KEY)
        x = Test.objects.all().count()
        print(x)
        print(type(x))
        self.s_id = s.dumps(x + 1)
        if self.pk is None:
            super(Test, self).save(self, *args, **kwargs)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return force_text(self.name)


class Question(models.Model):
    test = models.ForeignKey(Test)
    title = models.CharField(max_length=500, verbose_name= ('question'))
    correct_answer = models.CharField(max_length=50, verbose_name=('corr_ans'))
    ss_id = models.CharField(max_length=100, blank=True, null=False)

    def save(self, *args, **kwargs):
        from itsdangerous import URLSafeSerializer
        s = URLSafeSerializer(SECRET_KEY)
        x = datetime.now()
        self.ss_id = s.dumps(str(x))
        if self.pk is None:
            super(Question, self).save(self, *args, **kwargs)

    class Meta:
        verbose_name = ('question')
        verbose_name_plural = ('questions')

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

class Answer(models.Model):
    ques = models.ForeignKey(Question)
    ans = models.CharField(max_length=50, verbose_name=('ans'))

    class Meta:
        verbose_name = ('answer')
        verbose_name_plural = ('answers')

    def __unicode__(self):
        return self.pk

    def __str__(self):
        return force_text(self.pk)

    def __int__(self):
        return force_text(self.pk)

    def __str__(self):
        return force_text(self.pk)


class Choice(models.Model):
    test = models.ForeignKey(Test)
    ques = models.OneToOneField(Question, verbose_name= ('ques'))
    ans = models.OneToOneField(Answer, verbose_name= ('ans'),)
    user = models.ForeignKey(UserProfile, blank=True, null=True)

    # def __unicode__(self):
    #     return self.ans

    # def __int__(self):
    #     return force_text(self.ans.ans)

    def __str__(self):
        return force_text(self.ans.ans)

    # def __call__(self):
    #     return force_text(self.ans.ans)
    # verbose_name= ('choice')

    class Meta:
        verbose_name =  ('choice')


class Score_Card(models.Model):

    user = models.ForeignKey(UserProfile)
    test = models.ForeignKey(Test)
    score = models.IntegerField(default=0.00)
    disables = models.BooleanField(default=False,  null=False, blank=False)
    def __unicode__(self):
        return self.score

    def __int__(self):
        return force_text(self.score)


    def __str__(self):
        return force_text(self.score)

