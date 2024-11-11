import os
import random
from django.conf import settings
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
from playsound import playsound


# In-memory storage for teams
team_storage = {
    'Red': [],
    'Blue': []
}
equipment_storage = {} #Key will be player_id : equipment_ID

score_storage = {}

base_storage = {}

hit_messages = []

def initialize_player_score(player_id):
    score_storage[player_id] = 0 


### UDP Functionality
# UDP Configuration
UDP_IP = "255.255.255.255"  # Broadcast IP
UDP_PORT_BROADCAST = 7500   # Port for broadcasting
UDP_PORT_RECEIVE = 7501     # Port for receiving


def initialize_player_game(code):
    server_address = ("127.0.0.1", 7500)
    
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Send the start code
        sock.sendto(code.encode(), server_address)
        print(f"Sent: {code}")
    finally:
        sock.close()

def receive_udp_message():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", UDP_PORT_RECEIVE))
    while True:  # Use a loop to keep listening for messages
        data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
        print(f"Received data: {data.decode()} from {addr}")  # Debug print
        transmitting_equipment_id, hit_id = map(int, data.decode().split(':'))
        
        print(f"EquipmentId = {transmitting_equipment_id}, hitId = {hit_id}")
        #print(team_storage)
        #print(equipment_storage)
        
        # Find the player ID by the transmitting equipment ID
        player_id = next((pid for pid, eid in equipment_storage.items() if eid == transmitting_equipment_id), None)
        player = Player.objects.get(id=player_id)
        print(player)
        if hit_id == 53 or hit_id == 43:
            score_storage[player_id] += 100
            base_storage[player_id] = True
            hit_messages.append(f"{player.codename} hit the base!")
            print("Base hit by, returnng")
            print(base_storage)
            
        else:
        
            hit_player_id = next((pid for pid, eid in equipment_storage.items() if eid == hit_id), None)
            hit = Player.objects.get(id=hit_player_id)
            
            print(f"Player_id = {player_id}, hitID = {hit_player_id}")
         
            hit_team = 6
            player_team = 6
            for id in team_storage["Red"]:
                print(id.id)
                if hit_player_id == id.id:
                    hit_team = 5
                if player_id == id.id:
                    player_team = 5
		
                
            if player_id is not None:
                if True:
                    if hit_team == player_team:
                        # Deduct points for hitting a teammate
                        score_storage[player_id] -= 10
                        hit_messages.append(f"{player.codename} hit their own teammate, {hit.codename}")
                        print(f"Friendly fire: {player_team, hit_team}")
                    else: 
                        score_storage[player_id] += 10
                        hit_messages.append(f"{player.codename} hit {hit.codename}")
                        initialize_player_game(str(hit_player_id))
                        print(f"Updated score for player {player_id}. New score: {score_storage[player_id]}")
                else:
                    # Handle the case where one of the player IDs does not exist in the team_storage
                    print(f"Player ID {player_id} or Hit Player ID {hit_player_id} does not exist in team_storage.")
            else:
                 print(f"No player found for transmitting equipment ID {transmitting_equipment_id}.")
   
        

def trigger_udp_broadcast(request):
    server_address = ("127.0.0.1", 7500)
    
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Send the start code
        sock.sendto(b"221", server_address)
        sock.sendto(b"221", server_address)
        sock.sendto(b"221", server_address)
        print("Sent: 221 thrice")
    finally:
        sock.close()  
    return JsonResponse({"status": "success"})

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
       
            messages.success(request, f"Success: Player '{codename}' has been added.")
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
    
    # Prepare the context to pass to the template
    context = {
        'red_team': red_team,
        'blue_team': blue_team
    }
    
    return render(request, "index.html", context)
    

def hud_view(request):
    mp3_folder = os.path.join(settings.BASE_DIR, 'static', 'mp3s')
    
    # List all mp3 files in the folder
    mp3_files = [f for f in os.listdir(mp3_folder) if f.endswith('.mp3')]
    
    # Randomly select an mp3 file
    selected_mp3 = random.choice(mp3_files) if mp3_files else None
    
    # Retrieve players from the in-memory storage
    red_team = team_storage.get('Red', [])
    blue_team = team_storage.get('Blue', [])
    
    start_udp_broadcast()
    
    # Create a list of tuples with player and their corresponding score
    red_team = [(player, score_storage.get(player.id, 0), base_storage.get(player.id, 0)) for player in red_team]
    blue_team = [(player, score_storage.get(player.id, 0), base_storage.get(player.id, 0)) for player in blue_team]


	# Sort players by score in descending order
    red_team.sort(key=lambda x: x[1], reverse=True)
    blue_team.sort(key=lambda x: x[1], reverse=True)
    
    red_team_score = sum(score for _, score, _ in red_team)
    blue_team_score = sum(score for _, score, _ in blue_team)
    
    # Pass the context
    context = {
		'mp3_file': f'lasertag/mp3_folder/{selected_mp3}' if selected_mp3 else None,
        'red_team': red_team,
        'blue_team': blue_team,
        'hit_messages': hit_messages,  
        'base_storage': base_storage,
        'red_team_score': red_team_score,
        'blue_team_score': blue_team_score
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
            
            # Check if equipment ID is already in use
            if equipment_id in equipment_storage.values():
                messages.error(request, 'This equipment ID is already assigned to another player.')
                return redirect('assign_teams_equipment')  # Redirect back to the form

            # Assign the player to the specified team
            if team_name in team_storage:
                team_storage[team_name].append(player)
                equipment_storage[int(player_id)] = int(equipment_id)  # Assign equipment to the player
                score_storage[int(player_id)] = 0  # Initialize score to 0
                base_storage[int(player_id)] = False  # Initialize base storage
                initialize_player_game(equipment_id)
                print("Transmitting player ID")
                
                #Broadcast the equipment ID
                if player_id in equipment_storage:
                    transmitting_id = equipment_storage.get(player_id)
                    initialize_player_game(transmitting_id)
                    #broadcast_udp_message(f"{transmitting_id}:")  # Transmitting 

                messages.success(request, f"Assigned {player.codename} to {team_name} with Equipment ID: {equipment_id}")
            else:
                messages.error(request, f"Team '{team_name}' does not exist.")

        except Player.DoesNotExist:
            messages.error(request, f"Player with ID {player_id} does not exist.")

        return redirect('/assign_teams_equipment/')  # Redirect after handling

    return render(request, 'assign_teams_equipment.html')



def remove_players(request):
    # Clear the team and equipment storage
    for key in team_storage:
        team_storage[key] = []  # Assign an empty list to each key
    for key in equipment_storage:
        equipment_storage[key] = []  # Assign an empty list to each key

    messages.success(request, "All players have been removed from the current game.")
    return redirect('index')  # Redirect to the index page after clearing

def start_udp_broadcast():
    # Start a timer that runs udp_broadcast_function after 30 seconds
    timer = threading.Timer(30, send_start_code) #udp_broadcast_function
    timer.start()
    
    
def splash_screen(request):
    return render(request, 'splash_screen.html')

def update_score(player_id, score):
    # Update the score logic
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "score_updates",
        {
            'type': 'send_score_update',
            'score': score,
            'player_id': player_id,
        }
    )

def get_scores(request):
    # Retrieve players from the in-memory storage
    red_team_players = team_storage.get('Red', [])
    blue_team_players = team_storage.get('Blue', [])
    
    # Create a list of dictionaries with player details and their corresponding scores
    red_team = [
        {
            'id': player.id,
            'codename': player.codename,
            'score': score_storage.get(player.id, 0),
            'base': base_storage.get(player.id, 0)
        }
        for player in red_team_players
    ]
    
    blue_team = [
        {
            'id': player.id,
            'codename': player.codename,
            'score': score_storage.get(player.id, 0),
            'base': base_storage.get(player.id, 0)
        }
        for player in blue_team_players
    ]

    # Sort players by score in descending order
    red_team.sort(key=lambda x: x['score'], reverse=True)
    blue_team.sort(key=lambda x: x['score'], reverse=True)
    
    # Calculate team scores
    red_team_score = sum(player['score'] for player in red_team)
    blue_team_score = sum(player['score'] for player in blue_team)
    
    # Prepare data for JSON response
    data = {
        'red_team': red_team,
        'blue_team': blue_team,
        'hit_messages': hit_messages,
        'base_storage': base_storage,
        'red_team_score': red_team_score,
        'blue_team_score': blue_team_score
    }
    
    return JsonResponse(data)


def send_start_code():
    server_address = ("127.0.0.1", 7500)
    
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Send the start code
        sock.sendto(b"202", server_address)
        print("Sent: 202")
    finally:
        sock.close()


