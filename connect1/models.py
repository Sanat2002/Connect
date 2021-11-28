from django.db import models

class userverify(models.Model):
    name = models.CharField(max_length=20)
    token = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class userprofile(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    profile_pic = models.ImageField(blank=True,null=True)

    def __str__(self):
        return self.name