from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PlayerForm
from .models import Player
from django.contrib import messages

# In-memory storage for teams
team_storage = {
    'Red': [Player.objects.get(id=1)],
    'Blue': []
}
equipment_storage = {1:5, 2:10} #Key will be player_id : equipment_ID


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
            # Get the codename from the form data
            codename = form.cleaned_data['codename']
            if Player.objects.filter(codename=codename).exists():
                messages.error(request, f"Error: Player with codename '{codename}' already exists.")
                return redirect('/add_player/')  # Redirect to the same page
            player = form.save(commit=True)  # Save the player object and commit to DB
          
            team_name = request.POST.get('team')  # Get team from the form data
            add_player_to_team(player.id, team_name)  # Add player to the in-memory team
            
            messages.success(request, f"Success: Player '{codename}' has been added to the {team_name} team.")
            #return redirect('/hud/')  # Redirect to HUD view after adding the player
    else:
        form = PlayerForm()
    
    return render(request, 'add_player.html', {'form': form})

def view_players(request):
    players = Player.objects.all()
    return render(request, "view_players.html", {"players":players})

def index(request):
    # Fetch player IDs for each team from the team_storage
    red_team = team_storage.get('Red', [])
    blue_team = team_storage.get('Blue', [])

    # Retrieve players based on the IDs from the dictionary
    #equipment_ids = equipment_storage
    
    # Prepare the context to pass to the template
    context = {
        'red_team': red_team,
        'blue_team': blue_team
    }
    
    return render(request, "index.html", context)  # Render the template with the context


def hud_view(request):
    # Retrieve players from the in-memory storage
    red_team = team_storage.get('Red', [])
    blue_team = team_storage.get('Blue', [])

    # Add a dynamic hit message (replace this with your actual logic)
    """REPLACE WITH UDP FUNCTIONALITY"""
    hit_messages = [
        "Player 1 hit Player 2",
        "Player 3 hit Player 4",
        "Player 5 hit Player 6",
        "Player 7 hit Player 8",
        "Player 2 hit Player 5",
        
    ]  # You can replace this with actual logic for generating hit messages

    # Pass the hit message along with the teams to the context
    context = {
        'red_team': red_team,
        'blue_team': blue_team,
        'hit_messages': hit_messages  # Add the hit message to the context
    }
    return render(request, 'hud_view.html', context)
    
   
#Page to assign team and equipment for players joining game
def assign_teams_equipment(request):
    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        equipment_id = request.POST.get('equipment_id')
        team_name = request.POST.get('team')

        try:
            player = Player.objects.get(id=player_id)

            # Check if the player is already in the specified team
            if player in team_storage.get(team_name, []):
                messages.error(request, f"Error: Player '{player.codename}' is already assigned to the {team_name} team.")
                return redirect('/assign_teams_equipment/')  # Redirect to the same page

            # Check if the player is in the other team
            other_team = 'Red' if team_name == 'Blue' else 'Blue'
            if player in team_storage.get(other_team, []):
                messages.error(request, f"Error: Player '{player.codename}' cannot be assigned to both teams.")
                return redirect('/assign_teams_equipment/')  # Redirect to the same page

            # Assign the player to the specified team
            if team_name in team_storage:
                team_storage[team_name].append(player)
                equipment_storage[player_id] = equipment_id  # Assign equipment to the player

                messages.success(request, f"Assigned {player.codename} to {team_name} with Equipment ID: {equipment_id}")
            else:
                messages.error(request, f"Team '{team_name}' does not exist.")

        except Player.DoesNotExist:
            messages.error(request, f"Player with ID {player_id} does not exist.")

        return redirect('/assign_teams_equipment/')  # Redirect after handling

    return render(request, 'assign_teams_equipment.html')

