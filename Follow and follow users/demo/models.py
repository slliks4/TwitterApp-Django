from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(blank=True, null=True, upload_to='images')
    date_modified = models.DateTimeField(auto_now=True, blank=True)
    follows = models.ManyToManyField("self", related_name='followed_by',symmetrical=False,blank=True)
    def total_followers(self):
        return self.follows.count()
    class Meta:
        verbose_name_plural = 'Profile'
    def __str__(self) -> str:
        return f"{self.user}"

@receiver(post_save, sender=User)    
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()
