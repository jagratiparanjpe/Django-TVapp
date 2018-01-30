from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Prefetch, Q
#from django.views.generic.list_detail import object_list
from . import models

# admin view. list of all teams
@login_required()
def team_list(request):
    # All teams objects with annotation to get average team score
    teams_activity_score = models.Team.objects.all().annotate(average_score = Avg('Teams__Candidates__Scores__score'))
    template = 'Voiceapp/team_list.html'
    #template = 'Voiceapp/team_list_for_admin.html'

    context = {
        'score' : teams_activity_score
    }
    return render(request, template, context)

### Search functionality for admin. filter team by team name
@login_required()
def search(request):
    #template = 'Voiceapp/team_list_for_admin.html'
    template = 'Voiceapp/team_list.html'

    query = request.GET.get('q')
    if(query):
        teams_activity_score = models.Team.objects.filter(Q(team_name__icontains=query)).annotate(average_score = Avg('Teams__Candidates__Scores__score'))
    else:
        teams_activity_score = models.Team.objects.all().annotate(average_score=Avg('Teams__Candidates__Scores__score'))

    context = {
        'score' : teams_activity_score
    }
    return render(request, template, context)


## activity details of candidates for the team
@login_required()
def team_details(request,pk):

    team = models.Team.objects.get(pk=pk)
    candidate_activities=models.Activity.objects.select_related('candidate__team').filter(candidate__team=team)

    #template = 'Voiceapp/candidate_activity_list_per_team.html'
    template = 'Voiceapp/candidate_activity_list_per_team.html'

    context = {
        'team' : team,
        'candidate_activities' : candidate_activities
    }
    return render(request, template, context)


## lists the candidate for mentor template
class CandidateswithMentorListView(LoginRequiredMixin, ListView):
    model = models.Team
    template_name = 'Voiceapp/candidate_list_mentored_by_user.html'
    def get_queryset(self):
        result =models.Candidate.objects.select_related('team').filter(team__mentor=self.request.user)
        return result


# @login_required
def activity_list(request, pk):
    candidate = models.Candidate.objects.get(pk=pk)
    activities = models.Activity.objects.annotate(average_score=Avg('Scores__score')).filter(candidate = candidate)
    final_avearge_score = activities.aggregate(Avg('average_score'))

    candidate_activity_score = models.Candidate.objects.all().annotate(average_score=Avg('Candidates__Scores__score')) ## working correct

    template = 'Voiceapp/candidate_activity_details.html'
    context = {
        'candidate' : candidate,
        'activities': activities,
        'activity_score': candidate_activity_score,
        'final_score' : final_avearge_score['average_score__avg']
    }
    return render(request, template, context)


