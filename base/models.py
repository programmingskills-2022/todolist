from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField()
    checked=models.BooleanField(default=False ,null=False, blank=False)
    created=models.DateTimeField(auto_now=True)
    updated=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering=['-updated','-created']
