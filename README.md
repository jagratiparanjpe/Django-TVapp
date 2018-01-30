# Django-TVapp
Django project
Details
This is a management system to monitor the participants performance in the show.
This system has 3 types of users: an admin, mentors, and candidates.
Each candidate belongs to one of the mentors teams, while mentors on the other hand can mentor more than one team.
Each candidate gains scores for songs he/she performs. Each performance is scored by all the mentors on a scale of 0-100
The mentor can review the scores of the candidates in his teams 
The admin can review the scores of all the candidates in all the teams

At present only mentor and admin can login to the system and view the score, average score of candidate and teams.

This project supports management command ("populate_db") to populate different models of the system  
example usage: "python mange.py populate_db <no_of_metors> <no_of_candidate> <no_of_teams> <no_of_activities>"
