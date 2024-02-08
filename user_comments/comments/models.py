from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from .utilis import unique_slug_generator
from django.contrib.auth.models import User 

class Profile(models.Model):
    users = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile', null=True,blank=True)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(blank=True,null=True, upload_to='img')

    class meta:
        verbose_name_plural = 'Profile'
    
    def __str__(self) -> str:
        return f"{self.users}"
    
    def create_user_profile(sender, instance, created, **kwargs):
        if created and not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance)

choices=(('World','World'),('Friends','Friends'))
class Posts(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name='POSTS', blank=True, null= True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=100, choices=choices, null=True,blank=True)
    likes = models.ManyToManyField(User, related_name='posts', blank=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    slug = models.SlugField(blank=True)

    def total_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name_plural='Posts'
        ordering=('-date','-time')

    def __str__(self):
        return f'{self.title}'
    
def slug_generator(sender, instance, *args,**kwargs):
    if not instance.slug:
        instance.slug=unique_slug_generator(instance)

pre_save.connect(slug_generator,sender=Posts)

class Comments(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Comments'
        ordering=('-date','-time')

    def __str__(self) -> str:
        return f'{self.posts}'