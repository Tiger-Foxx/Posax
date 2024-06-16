from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.

class Artiste(AbstractUser):
    username = models.CharField(max_length=13, unique=True) # il s'agit ici en realite de son email
    email = models.EmailField()
    password = models.CharField(max_length=500)
    nom=models.CharField(max_length=200,null=True,blank=True)
    bio=models.TextField(blank=True,null=True)
    whatsapp = models.CharField(max_length=13,null=True,blank=True)
    facebook = models.CharField(max_length=300,null=True,blank=True)
    instagram = models.CharField(max_length=300,null=True,blank=True)
    email_verified = models.BooleanField(default=False)
    photo=models.ImageField(upload_to='Photo de profils')
    #champs non editables
    date=models.DateField(auto_now=True,editable=False)
    def __str__(self):
        return f"Artiste | nom: {self.nom} | whatsapp: {self.whatsapp}"
