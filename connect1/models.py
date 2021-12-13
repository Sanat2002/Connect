from django.db import models
import datetime
import os

# so to save the uploaded images in specific folder with unique name
def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)

class userverify(models.Model):
    name = models.CharField(max_length=20)
    token = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class userprofile(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    profile_pic = models.ImageField(upload_to=filepath,blank=True,null=True)
    bio = models.CharField(max_length=200,blank=True)
    phoneno = models.BigIntegerField(blank=True,default=0)
    gender = models.CharField(blank=True,max_length=10)
    toaddpost = models.ImageField(upload_to=filepath,blank=True,null=True)
    posts = models.JSONField(default=dict) # user jsonField in order to store lists,map,dict
    connections = models.JSONField(default=dict)
    connectionrequests = models.JSONField(default=dict)
    pendingconnections = models.JSONField(default=dict)

    def __str__(self):
        return self.name