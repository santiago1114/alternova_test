from django.db import models

class Type(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name

class Stream(models.Model):
    name = models.CharField(max_length=255, help_text="Register the name")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,
                               help_text="Select the genre")
    type = models.ForeignKey(Type, on_delete=models.CASCADE,
                             help_text="Select the type")
    views = models.BigIntegerField(editable=False, default=0)
    score = models.DecimalField(blank=True, null=True, max_digits=1, decimal_places=1)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['name']
    