from django.db import models

from Comptes.models import Artiste

# Create your models here.
class Post(models.Model):
    date=models.DateField(auto_now=True,editable=False)
    Auteur=models.ForeignKey(Artiste,on_delete=models.CASCADE)
    titre=models.CharField(max_length=500) 
    def __str__(self):
        return f"POST DE  : {self.Auteur.nom} LE {self.date}"
class Oeuvre(Post):
    categorie=models.CharField(max_length=800)
    Photo1=models.ImageField(upload_to='PhotosOeuvre')
    Photo2=models.ImageField(blank=True,upload_to='PhotoOeuvre',null=True)
    Photo3=models.ImageField(blank=True,upload_to='PhotoOeuvre',null=True)
    Photo4=models.ImageField(blank=True,upload_to='PhotoOeuvre',null=True)
    
    def __str__(self):
        return f"OEUVRE DE L'ARTISTE : {self.Auteur.nom} POSTEE LE {self.date} | TITRE {self.titre}" 
    
class Article(Post):
    Photo=models.ImageField(upload_to='PhotosArticle')
    intro=models.TextField(blank=True , null=True)
    paragraphe1=models.TextField()
    paragraphe2=models.TextField(blank=True , null=True)

    def __str__(self):
        return f"ARTICLE  DE L'ARTISTE : {self.Auteur.nom} ECRIT LE {self.date} | TITRE {self.titre}" 