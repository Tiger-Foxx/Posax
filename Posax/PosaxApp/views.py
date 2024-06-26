from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Oeuvre
from Comptes.models import Artiste
# Create your views here.


CATEGORIES = [
    'Architecture', 'Collage', 'Dessin', 'Gravure', 'Immobilier', 'Installation', 'Land Art',
    'Mosaïque', 'Peinture', 'Performance', 'Photographie', 'Sculpture', 'Street Art', 'Textile', 'Vidéo', 'Autre'
]

def index(request):
    articles=Article.objects.all().order_by('-date')
    return render(request, 'PosaxApp/index.html',context={'articles': articles})

def about(request):
    return render(request, 'PosaxApp/about-us.html')




@login_required
def publier_oeuvre(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        categories = request.POST.getlist('choice')
        categorie = " ".join(categories)
        photo1 = request.FILES.get('photo1')
        photo2 = request.FILES.get('photo2', photo1)
        photo3 = request.FILES.get('photo3', photo1)
        photo4 = request.FILES.get('photo4', photo1)
        
        oeuvre = Oeuvre(
            Auteur=request.user,
            titre=titre,
            categorie=categorie,
            Photo1=photo1,
            Photo2=photo2,
            Photo3=photo3,
            Photo4=photo4,
        )
        oeuvre.save()
        return redirect('index')  # Rediriger vers une page de succès ou la page principale
    
    return render(request, 'PosaxApp/posterOeuvre.html')  # Remplacer 'votre_template.html' par le nom du template approprié


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Article
from Comptes.models import Artiste

@login_required
def publier_article(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        photo = request.FILES.get('photo1')
        intro = request.POST.get('intro')
        paragraphe1 = request.POST.get('paragraphe1')
        paragraphe2 = request.POST.get('paragraphe2')
        
        article = Article(
            Auteur=request.user,
            titre=titre,
            Photo=photo,
            intro=intro,
            paragraphe1=paragraphe1,
            paragraphe2=paragraphe2,
        )
        article.save()
        return redirect('index')  # Rediriger vers une page de succès ou la page principale
    
    return render(request, 'PosaxApp/posterArticle.html')  # Remplacer 'votre_template_article.html' par le nom du template approprié

from django.shortcuts import render, get_object_or_404

def DetailArtiste(request, id):
    artist = get_object_or_404(Artiste, id=id)
    artworks = Oeuvre.objects.filter(Auteur=artist)
    articles = Article.objects.filter(Auteur=artist)
    
    # Organiser les œuvres par catégories
    categories = {}
    for artwork in artworks:
        for category in artwork.categorie.split(' '):  # Supposons que les catégories soient séparées par des espaces
            if category not in categories:
                categories[category] = []
            categories[category].append(artwork)
    
    # Limiter le premier paragraphe des articles à 150 caractères
    for article in articles:
        article.paragraphe1 = article.paragraphe1 [:80] + '...' if len(article.paragraphe1 ) > 150 else article.paragraphe1 
    
    context = {
        'artist': artist,
        'categories': categories,
        'articles': articles,
    }
    return render(request, 'PosaxApp/detailArtiste.html', context)

def liste_artistes(request):
    artistes = Artiste.objects.all()
    return render(request, 'PosaxApp/ListeArtistes.html', {'artistes': artistes})


def detail_article(request,id):
    article=get_object_or_404(Article,id=id)
    return render(request, 'PosaxApp/ArticleDetail.html', {'article': article})


from django.db.models import Q


def Recherche(request):
    sujet=request.POST.get('sujet')
    
    artworks = Oeuvre.objects.filter(
    Q(titre__icontains=sujet) | 
    Q(Auteur__nom__icontains=sujet) | 
    Q(categorie__icontains=sujet)
    ).order_by('-date')

    articles = Article.objects.filter(
    Q(titre__icontains=sujet) | 
    Q(Auteur__nom__icontains=sujet)
    ).order_by('-date')

    # Organiser les œuvres par catégories
    categories = {}
    for artwork in artworks:
        for category in artwork.categorie.split(' '):  # Supposons que les catégories soient séparées par des espaces
            if category not in categories:
                categories[category] = []
            categories[category].append(artwork)
    
    # Limiter le premier paragraphe des articles à 150 caractères
    for article in articles:
        article.paragraphe1 = article.paragraphe1 [:80] + '...' if len(article.paragraphe1 ) > 150 else article.paragraphe1 
    
    context = {
        'sujet':sujet,
        'categories': categories,
        'articles': articles,
    }
    return render(request, 'PosaxApp/publications.html', context)
