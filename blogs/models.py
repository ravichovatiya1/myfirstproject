from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.utils import timezone

# Create your models here.

# class User(AbstractUser):
    # PhNumber = models.PositiveIntegerField(min_length=10,max_length = 10)


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
    Prof_url = models.URLField()
    Img_pic = models.ImageField(upload_to = 'profile_pic/%Y/%m/%d/')

    def __str__(self):
        return self.user.username



# this is the library to import for this task
from django.urls import reverse

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    Title = models.CharField(max_length=50)
    Text = models.TextField()
    Created_date = models.DateTimeField(default= timezone.now)
    Published_date = models.DateTimeField(blank=True,null=True)

    def published(self):
        self.Published_date = timezone.now()
        self.save()

    def drafted(self):
        self.Published_date = None
        self.save()

    def get_absolute_url(self):
        return reverse("app:post_detail", kwargs={"pk": self.pk})
    

    def __str__(self):
        return self.Title + ' ' + self.author.username + ' ' + str(self.pk)



class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    Author = models.CharField(max_length=256)
    Text = models.TextField()

    def __str__(self):
        return self.Author