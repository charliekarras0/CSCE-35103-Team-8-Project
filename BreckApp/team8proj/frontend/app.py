import os
import sys
import tkinter as tk  
from PIL import Image, ImageTk 

import django  # Import Django

# Set up the path to your project
path = os.getcwd()
split = path.split('/')
path = split[:-1]
path = '/'.join(path)

sys.path.append(path)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team8proj.settings')

# Initialize Django
django.setup()

# Now you can import your models
from lasertag.models import Player
from networking.udp import UDP



# Create F5 play action game screen
def play_action_display(event):
	# Create new window for displaying players
	play_action_display_window = tk.Tk()
	play_action_display_window.title("Game Action")
	play_action_display_window.geometry("400x400")
	
	# Implement Countdown screen
	""""""
	
	# Create label for window
	label = tk.Label(play_action_display_window, text="All Players C", font=("Arial", 20))
	label.pack(pady=10)
	
	#Create listbox to display players
	player_listbox = tk.Listbox(play_action_display_window, width=50, height=15)
	
	# Fetch all players from the database
	players = Player.objects.all()
	
	# Insert into listbox
	for player in players:
		player_listbox.insert(tk.END, f"ID: {player.id}, Codename: {player.codename}")
		
	# Start mainloop
	play_action_display_window.mainloop()
	




# Player entry window
def create_player_entry_window():
    global udp
    udp = UDP()
    player_entry_window = tk.Tk()
    player_entry_window.title("Player Entry")
    player_entry_window.geometry("400x400")  # window size

    label = tk.Label(player_entry_window, text="Player Entry", font=("Arial", 24))
    label.pack(pady=20)

    # Player entry
    form_frame = tk.Frame(player_entry_window)
    form_frame.pack(pady=10)

    # Player ID box
    tk.Label(form_frame, text="Player ID:").grid(row=0, column=0)
    player_id_entry = tk.Entry(form_frame)
    player_id_entry.grid(row=0, column=1)

    # Codename box
    tk.Label(form_frame, text="Codename:").grid(row=1, column=0)
    codename_entry = tk.Entry(form_frame)
    codename_entry.grid(row=1, column=1)

    # Equipment ID box
    tk.Label(form_frame, text="Equipment ID:").grid(row=2, column=0)
    equipment_id_entry = tk.Entry(form_frame)
    equipment_id_entry.grid(row=2, column=1)

    # Add player button
    submit_button = tk.Button(player_entry_window, text="Add Player", command=lambda: add_player(player_id_entry.get(), codename_entry.get(), equipment_id_entry.get()))
    submit_button.pack(pady=20)
    
    # Start Game with F5 
    player_entry_window.bind("<F5>", play_action_display)
    
    # View all players with 'a'
    #player_entry_window.bind("<a>", view_players)
    

    player_entry_window.mainloop()

# Basic add player function
def add_player(player_id, codename, equipment_id):
    print(f"Player Added: ID: {player_id}, Codename: {codename}, Equipment ID: {equipment_id}")
    try:
        global udp
        udp.transmit_equipment_id(equipment_id=int(equipment_id))

        # Save player to the database
        new_player = Player(id=int(player_id), codename=codename)
        new_player.save()  # Save the player to the database
    except ValueError:
        print("Equipment ID must be an integer")
        
# Splash screen
def splash_screen():
    splash = tk.Tk()  
    splash.title("Splash Screen")
    splash.geometry("400x400") 
    
    # Path for splash image
    current_dir = os.path.dirname(__file__) 
    img_path = os.path.join(current_dir, "logo.jpg")  

    # Load splash image
    img = Image.open(img_path) 
    img = img.resize((400, 400), Image.LANCZOS)  # Size
    splash_image = ImageTk.PhotoImage(img)
    
    splash_label = tk.Label(splash, image=splash_image)
    splash_label.pack()

    splash.after(3000, splash.destroy)  # Destroy splash screen after 3 seconds

    splash.mainloop()  # Display splash

# Run splash screen
splash_screen()

# Then create main window
create_player_entry_window()
