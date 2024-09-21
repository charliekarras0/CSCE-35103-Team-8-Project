import tkinter as tk
from PIL import Image, ImageTk  
import os

# Player entry window
def create_player_entry_window():
    player_entry_window = tk.Tk()
    player_entry_window.title("Player Entry")
    player_entry_window.geometry("400x400")  #window size

    label = tk.Label(player_entry_window, text="Player Entry", font=("Arial", 24))
    label.pack(pady=20)

    # player entry
    form_frame = tk.Frame(player_entry_window)
    form_frame.pack(pady=10)

    # player ID box
    tk.Label(form_frame, text="Player ID:").grid(row=0, column=0)
    player_id_entry = tk.Entry(form_frame)
    player_id_entry.grid(row=0, column=1)

    # codename box
    tk.Label(form_frame, text="Codename:").grid(row=1, column=0)
    codename_entry = tk.Entry(form_frame)
    codename_entry.grid(row=1, column=1)

    # equipment ID box
    tk.Label(form_frame, text="Equipment ID:").grid(row=2, column=0)
    equipment_id_entry = tk.Entry(form_frame)
    equipment_id_entry.grid(row=2, column=1)

    # add player button
    submit_button = tk.Button(player_entry_window, text="Add Player", command=lambda: add_player(player_id_entry.get(), codename_entry.get(), equipment_id_entry.get()))
    submit_button.pack(pady=20)

    player_entry_window.mainloop()

# basic add player function
def add_player(player_id, codename, equipment_id):
    print(f"Player Added: ID: {player_id}, Codename: {codename}, Equipment ID: {equipment_id}")

# splash screen
def splash_screen():
    splash = tk.Tk()
    splash.title("Splash Screen")
    splash.geometry("400x400") 
    
    # path for photon splash image
    current_dir = os.path.dirname(__file__) 
    img_path = os.path.join(current_dir, "logo.jpg")  

    # load photon splash image
    img = Image.open(img_path) 
    img = img.resize((400, 400), Image.LANCZOS)  # size
    splash_image = ImageTk.PhotoImage(img)
    
    splash_label = tk.Label(splash, image=splash_image)
    splash_label.pack()

    splash.after(3000, splash.destroy)  # destroy splash screen after 3 seconds

    splash.mainloop()  # display splash

# run splash screen
splash_screen()

# then create main window
create_player_entry_window()
