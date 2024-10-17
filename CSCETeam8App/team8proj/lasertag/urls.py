from django.urls import path, re_path
from . import views

urlpatterns = [
	path('', views.splash_screen, name='splash_screen'),  # Show splash screen on the root URL
    path("index", views.index, name="index"),
    re_path(r'^add_player/?$', views.add_player, name='add_player'),
    re_path(r'^view_players/?$', views.view_players, name="view_players"),
    path("hud/", views.hud_view, name="hud_view"),  # New HUD view URL
    path('assign_teams_equipment/', views.assign_teams_equipment, name='assign_teams_equipment'), 
    path('remove_players/', views.remove_players, name='remove_players'),
]
