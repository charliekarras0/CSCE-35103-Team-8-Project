from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PlayerForm
from .models import Player
from django.contrib import messages
import socket
import threading
from django.shortcuts import render
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# In-memory storage for teams
team_storage = {
    'Red': [Player.objects.get(id=1)],
    'Blue': []
}
equipment_storage = {1:5} #Key will be player_id : equipment_ID

score_storage = {1:0}
def initialize_player_score(player_id):
    score_storage[player_id] = 0 


### UDP Functionality
# UDP Configuration
UDP_IP = "255.255.255.255"  # Broadcast IP
UDP_PORT_BROADCAST = 7500   # Port for broadcasting
UDP_PORT_RECEIVE = 7501     # Port for receiving

# Function to send the UDP message
def broadcast_udp_message(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(message.encode(), (UDP_IP, UDP_PORT_BROADCAST))
    sock.close()

def receive_udp_message():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", UDP_PORT_RECEIVE))
    while True:  # Use a loop to keep listening for messages
        data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
        print(f"Received data: {data.decode()} from {addr}")  # Debug print
        equipment_id_transmitting, equipment_id_hit = map(int, data.decode().split(':'))
        
        # Update the score of the transmitting player
        if equipment_id_transmitting in score_storage:
            score_storage[equipment_id_transmitting] += 15
            print(f"Updated score for equipment {equipment_id_transmitting}: {score_storage[equipment_id_transmitting]}")  # Debug print
        else:
            print(f"No player found for transmitting equipment ID {equipment_id_transmitting}.")
        
        send_score_update_via_websocket()  # Send updated scores via WebSocket


def send_score_update_via_websocket():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "hud_updates",
        {
            "type": "send_score_update",
            "scores": score_storage,
        }
    )
    print(f"Sent score update via WebSocket: {score_storage}")  # Debug print

        
def update_player_score_from_udp(message):
    try:
        transmitting_equipment_id, _ = message.split(':')
        transmitting_equipment_id = int(transmitting_equipment_id)

        # Find the player ID by the transmitting equipment ID
        player_id = next((pid for pid, eid in equipment_storage.items() if eid == transmitting_equipment_id), None)

        if player_id is not None:
            # Increase the score by 15
            score_storage[player_id] += 15
            print(f"Updated score for player {player_id}. New score: {score_storage[player_id]}")
        else:
            print(f"No player found for transmitting equipment ID {transmitting_equipment_id}.")
    except ValueError as e:
        print(f"Error parsing message '{message}': {e}")


# Start the UDP receiver in a separate thread
def start_udp_listener():
    threading.Thread(target=receive_udp_message, daemon=True).start()

# Call this function at the start of your Django application
start_udp_listener()



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
            score_storage[player.id] = 0
            
            #Broadcast equipmentID
            equipment_id = equipment_storage.get(player.id)
            
            broadcast_udp_message(f"{equipment_id}") # Transmitting startup code to equipment
            
            messages.success(request, f"Success: Player '{codename}' has been added to the {team_name} team.")
            return redirect('/index')  # Redirect to HUD view after adding the player
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
    
    start_udp_broadcast()
    
    # Create a list of tuples with player and their corresponding score
    red_team = [(player, score_storage.get(player.id, 0)) for player in red_team]
    blue_team = [(player, score_storage.get(player.id, 0)) for player in blue_team]

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
                score_storage[player_id] = 0  # Initialize score to 0
                
                #Broadcast the equipment ID
                if player_id in equipment_storage:
                    transmitting_id = equipment_storage.get(player_id)
                    broadcast_udp_message(f"{transmitting_id}:")  # Transmitting 

                messages.success(request, f"Assigned {player.codename} to {team_name} with Equipment ID: {equipment_id}")
            else:
                messages.error(request, f"Team '{team_name}' does not exist.")

        except Player.DoesNotExist:
            messages.error(request, f"Player with ID {player_id} does not exist.")

        return redirect('/assign_teams_equipment/')  # Redirect after handling

    return render(request, 'assign_teams_equipment.html')



def remove_players(request):
    # Clear the team and equipment storage
    team_storage.clear()
    equipment_storage.clear()
    # Optionally, you can display a success message
    messages.success(request, "All players have been removed from the current game.")
    return redirect('index')  # Redirect to the index page after clearing
    
def udp_broadcast_function():
    # Broadcast startup code
    broadcast_udp_message("202")
    print("UDP Code Broadcasted")  # Example placeholder for actual broadcasting logic

def start_udp_broadcast():
    # Start a timer that runs udp_broadcast_function after 30 seconds
    timer = threading.Timer(30, udp_broadcast_function)
    timer.start()
    
    
def splash_screen(request):
    return render(request, 'splash_screen.html')

