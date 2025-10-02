from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm


def home_view(request):
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'about.html')

def dash_view(request):
    return render(request, 'dash.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # ou la page d'accueil que tu veux
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde l'utilisateur
            messages.success(request, "Compte créé avec succès ! Tu peux maintenant te connecter.")
            return redirect('login')  # Redirige vers la page de connexion
    else:
        form = SignUpForm()

    return render(request, 'auth/signup.html', {'form': form})

