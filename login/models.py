from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#Modelo que creara en la base de datos :v 
class Task(models.Model):
    Title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    FechaCompletada =models.DateTimeField(null=True)
    Importante = models.BooleanField(default=False)
    #Relacion de tablas :v 
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.Title + '-' + self.user.username