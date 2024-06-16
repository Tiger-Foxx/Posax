from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth import get_user_model,login,logout,authenticate

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

from Comptes.models import Artiste

User = get_user_model()

def inscription(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nom = request.POST.get('nom')
        whatsapp = request.POST.get('whatsapp')
        photo = request.FILES.get('photo')

        try:
            user = User.objects.create_user(username=email, email=email, password=password, nom=nom, whatsapp=whatsapp, photo=photo)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activez votre compte.'
            message = render_to_string('Comptes/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [email])

            return JsonResponse({"success": True, "redirect_url": "confirmation/"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    else:
        return render(request, "Comptes/auth.html")

def confirmation(request):
    return render(request, 'Comptes/confirmation_message.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.email_verified = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'Comptes/activation_invalid.html')

    
    

def connexion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember = request.POST.get('remember-me')
        print(f"password {password}")
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            if remember:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)
            return JsonResponse({"success": True, "redirect_url": "/"})
        else:
            return JsonResponse({"success": False, "message": "Nom d'utilisateur ou mot de passe incorrect."})
    else:
        return render(request, 'Comptes/auth.html')
    

def deconnexion(request):
    logout(request)
    return render(request,'Comptes/auth.html')


    
    
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password


@login_required
def profile(request, id):
    utilisateur = get_object_or_404(Artiste, id=id)
    
    if request.user.id != utilisateur.id:
        return redirect('connexion')
    
    if request.method == 'POST':
        name = request.POST.get("nom")
        email = request.POST.get("email")
        whatsapp = request.POST.get("whatsapp")
        facebook = request.POST.get("facebook")
        instagram = request.POST.get("instagram")
        bio = request.POST.get("bio")
        password = request.POST.get("password")
        photo = request.FILES.get("photo")

        utilisateur.nom = name
        utilisateur.email = email
        utilisateur.whatsapp = whatsapp
        utilisateur.facebook = facebook
        utilisateur.instagram = instagram
        utilisateur.bio = bio

        if photo:
            utilisateur.photo = photo

        if password:
            utilisateur.password = make_password(password)
        
        utilisateur.save()
        return redirect('index')
    
    return render(request, 'Comptes/Profile.html', {'utilisateur': utilisateur})


    

