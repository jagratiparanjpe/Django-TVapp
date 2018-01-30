from django.conf.urls import url
from . import views

app_name = 'Voiceapp'

urlpatterns = [
    ## url pattern for admin view
    url(r'myteams/$', views.team_list, name='my_teams'),
    url(r'myteams/(?P<pk>\d+)$', views.team_details, name='team_candidate'),
    ## search functionality for admin
    url(r'results/$', views.search, name= 'search'),

    ## url pattern for candidate view
    url(r'mycandidates/$', views.CandidateswithMentorListView.as_view(), name='my_candidates'),
    url(r'mycandidates/(?P<pk>\d+)$', views.activity_list, name='my_activities'),

]
