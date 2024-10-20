# CSCE-35103-Team-8-Project
Team 8's repository for the group project

# Github Usernames / Real Names
| GitHub Username   | Name                 |
|-------------------|----------------------|
| darias31          | Daria Stepanova      |
| victorberrios2341 | Victor Berrios       |
| charliekarras0    | Charlie Karras       |
| ludaChris2023     | Christopher Heffernan|
| br1husong         | Breck Husong         |

# Laser Tag Game

This project implements a Laser Tag game system with a Python/Django webpage app.

## Setup Instructions

1. Clone this repository using ssh key https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent, ```git clone git@github.com:charliekarras0/CSCE-35103-Team-8-Project.git```
	Alternatively, just download the file CSCETeam8App as a zip file and extract it to CSCETeam8App
2. Open project 
	Run: cd Downloads/CSCETeam8App/CSCETeam8App/
	*Assuming you downloaded the file into the Downloads folder. If not, adapt appropriately: cd path_to_dir/CSCETeam8App/CSCETeam8App*
3. Install python
	Run: sudo apt install python3
4. Install pip 
	Run: sudo apt install python3-pip
5. Create virtual environment
    Run: sudo apt install python3.11-venv
    Run: python3 -m venv photonvenv
    Run: source photonvenv/bin/activate
6. Install necessary packages
	Run: pip install -r requirements.txt
7. Prime django for the database *Note that this doesn't effect the postgres database, it only tells Django how the database is formatted. This can be confirmed through the postgres terminal*:
	Run: cd team8proj/
	Run: python manage.py migrate
		if this draws an error, 
			run: python manage.py migrate --fake
8. Start application:
	Run: python manage.py runserver
    Visit http://127.0.0.1:8000/ in your web browser to access the application
