from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Member(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=32)
    email    = models.EmailField()

    def __unicode__(self):
        return self.username

    class Meta:
        ordering = ['-id']

class Tag(models.Model):
    tag_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.tag_name

    def get_absolute_url(self):
        return '/bbs/post/tag/%s' % self.tag_name

class Post(models.Model):
    subject = models.CharField(max_length=255)
    content = models.TextField()
    author  = models.ForeignKey(User)
    created = models.DateTimeField(default=datetime.datetime.now, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    parent  = models.ForeignKey('self', null=True, blank=True)
    tags    = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.subject

    def get_absolute_url(self):
        return '/bbs/post/%d' % self.id

    class Meta:
        #db_table = ''
        ordering = ['-updated']

