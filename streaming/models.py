from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['name']

class Type(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['name']

class Stream(models.Model):
    name = models.CharField(max_length=255, help_text="Register the name")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,
                               help_text="Select the genre")
    type = models.ForeignKey(Type, on_delete=models.CASCADE,
                             help_text="Select the type")
    views = models.BigIntegerField(editable=False, default=0)
    score = models.DecimalField(blank=True, null=True, max_digits=2, decimal_places=1)
        
    def save(self, *args, **kwargs):
        # Calculate the mean of score before saving
        if self.pk:  # Check if the instance is already saved (updating)
            old_instance = Stream.objects.get(pk=self.pk)
            if self.score and old_instance.score:  # Check if exist score
                # Calculate the mean of score
                self.score = (old_instance.score + self.score)/2
        
        super(Stream, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['name']

class UserStreamDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stream = models.OneToOneField(Stream, on_delete=models.CASCADE)
    is_viewed = models.BooleanField(default=False)
    is_scored = models.BooleanField(default=False)