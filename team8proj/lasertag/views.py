from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PlayerForm
from .models import Player

# In-memory storage for teams
team_storage = {
    'Red': [],
    'Blue': []
}

def add_player_to_team(player_id, team_name):
	
	try:
		player = Player.objects.get(id=player_id)
		team_storage[team_name].append(player)  
	except Player.DoesNotExist:
		# Handle the case where the player doesn't exist
		print(f"Player with ID {player_id} does not exist")
		## You can either return an error message or redirect the use
    #player = Player.objects.get(id=player_id)  # Get player by ID from the database
    
	#team_storage[team_name].append(player)  # Add player to the in-memory team



"""def add_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PlayerForm()
    
    return render(request, 'add_player.html', {'form': form})"""
    
def add_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=True)  # Save the player object but don't commit to DB yet
            team_name = request.POST.get('team')  # Get team from the form data
            add_player_to_team(player.id, team_name)  # Add player to the in-memory team
            return redirect('/hud/')  # Redirect to HUD view after adding the player
    else:
        form = PlayerForm()
    
    return render(request, 'add_player.html', {'form': form})

def view_players(request):
    players = Player.objects.all()
    return render(request, "view_players.html", {"players":players})

def index(request):
    return render(request, "index.html")


def hud_view(request):
    # Retrieve players from the in-memory storage
    red_team = team_storage.get('Red', [])
    blue_team = team_storage.get('Blue', [])

    context = {
        'red_team': red_team,
        'blue_team': blue_team
    }
    return render(request, 'hud_view.html', context)
