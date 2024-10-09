from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PlayerForm
from .models import Player

def add_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PlayerForm()
    
    return render(request, 'add_player.html', {'form': form})

def view_players(request):
    players = Player.objects.all()
    return render(request, "view_players.html", {"players":players})

def index(request):
    return render(request, "index.html")
