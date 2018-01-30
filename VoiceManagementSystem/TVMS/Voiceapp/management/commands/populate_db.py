from django.core.management.base import BaseCommand, CommandError
from Voiceapp.models import Team, Candidate, Activity, ActivityScore_by_mentor
from django.db.models.base import ObjectDoesNotExist
from django.contrib.auth.models import User
import random
from faker import Faker
import datetime
""" Command to Poulate Database. This command expects following positional arguments respectively to populate database.
    mentor, candidate, team, activity
    Usage python manage.py populate_db <arguments>
    example: python manage.py populate_db 3 4 5 6
    this will create 3 mentors, 4 candidates, 5 teams, 6 activities in database.

"""


class Command(BaseCommand):
    help = 'Populate different models for the Voiceapp. Coomand expects following positional arguments:' \
           'number of mentor, number of ca  ndidate, number of teams, number of activities'


    def add_arguments(self, parser):
        parser.add_argument(
            'mentors',help='No of mentors to be created',nargs='?',type=int,default=3)
        parser.add_argument(
            'candidates', help='No of candidates to be created', nargs='?',type=int,default=5)

        parser.add_argument(
        'teams', help='No of teams to be created', nargs='?',type=int, default = 3)

        parser.add_argument(
        'activities', help='No of activities to be created', nargs='?', type=int, default=10)

    def handle(self, *args, **options):

        if User.objects.filter(username='admin').count() == 0:
            u = User(username='admin')
            u.set_password('admin@matific')
            u.is_superuser = True
            u.is_staff = True
            u.save()
            print("admin with username = admin and password = admin@matific created" )
        else:
            print("admin with username = admin and password = admin@matific already exists" )

        No_of_mentors = options['mentors']
        No_of_candidates = options['candidates']
        No_of_Teams = options['teams']
        No_of_Activities = options['activities']

        fakegen = Faker()
        mentor_list = []
        team_list = []
        candidate_list = []
        print("No_of_mentors="+str(No_of_mentors))
        print("No_of_activities=" + str(No_of_Activities))
        print("No_of_candidates=" + str(No_of_candidates))
        print("No_of_teams=" + str(No_of_Teams))
        for entry in range(No_of_mentors):
            # Create new Mentor Entry
            fake_user_name = fakegen.user_name()
            fake_name = fakegen.name().split()
            fake_first_name = fake_name[0]
            fake_last_name = fake_name[1]
            fake_email = fake_first_name+"."+fake_last_name+"@matific.com"

            user = User.objects.create_user(fake_user_name, fake_email, fake_user_name+'_123')
            print("Mentor with username = "+fake_user_name + " and password = "+ fake_user_name+"_123 created.")
            mentor_list.append(user)

        for team_no in range(No_of_Teams):

            #Create new Team object
            team_name = 'Team'+str(team_no+1)
            team = Team(team_name=team_name, mentor=random.choice(mentor_list))
            team.save()
            team_list.append(team)

        for can in range(No_of_candidates):
            candidate_name = fakegen.name()
            candidate = Candidate(candidate_name=candidate_name, team = random.choice(team_list))
            candidate.save()
            candidate_list.append(candidate)


        for act in range(No_of_Activities):
             # Used sentence() as couldn't find appropriate method to generate the song name
             song_name = "Song__"+str(fakegen.random_int())
             Date_of_performance = fakegen.date_between(datetime.date(2017,1,1), datetime.date(2018,1,1))
             activity = Activity(song_name=song_name, Date_of_performance=Date_of_performance,candidate=random.choice(candidate_list))
             activity.save()


             for m in mentor_list:
                 activity_score=ActivityScore_by_mentor(activity=activity, mentor=m, score=random.randint(1, 100))
                 activity_score.save()


