# CSCE-35103-Team-8-Project
Team 8's repository for the group project

# Github Usernames / Real Names
| GitHub Username   | Name   |
|------------|------------|
| darias31 | Daria Stepanova |
| victorberrios2341 | Victor Berrios |
| charliekarras0 | Charlie Karras |
| ludaChris2023 | Christopher Heffernan|
| br1husong | Breck Husong |

# Laser Tag Game

This project implements a Laser Tag game system with a Python/Django backend.

## Setup Instructions

1. Clone this repository using ssh key https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent, ```git clone git@github.com:charliekarras0/CSCE-35103-Team-8-Project.git```
2. Open project ```cd CSCE-35103-Team-8-Project```
3. Run ```python3 --version``` to verify python installation, if python not found run
```sudo apt install python3```
4. Install pip, run
```sudo apt install python3-pip```
5. (Optional) Create virtual environment, go to where the project was cloned in terminal using cd "path/to/project"
      run
   ```sudo apt install python3.11-venv```
      then once installed,
   ```python3 -m venv nameofvenv```
      finally
   ```source nameofvenv/bin/activate```
6. Run, ```pip install -r requirements.txt```, to install necessary packages
7. Set up the database by running, ```python manage.py migrate```
9. Run the application by running, ```python manage.py runserver```, visit http://127.0.0.1:8000/ in your web browser to access the application

## How to play
1. Launch the application.
   - Open **two instances of the terminal**:
     - In the **first terminal**, naviagate to the first team8proj directory and start the database server:
       ```
       cd path/to/CSCE-35103-Team-8-Project/team8proj
       python manage.py runserver
       ```
     - In the **second terminal**, navigate to the frontend directory and run the front end:
       ```
       cd path/to/CSCE-35103-Team-8-Project/team8proj/frontend
       python3 app.py
       ```
2. Use the player entry screen to add players by entering their IDs and codenames.
3. Players will be added to the database and can be viewed through the player viewing screen.
