from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models import Avg
from statistics import mean
# Create your models here.

class Team(models.Model):
    team_name = models.CharField(max_length=256)
    mentor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.team_name

class Candidate(models.Model):
    candidate_name = models.CharField(max_length=256)
    team = models.ForeignKey(Team, related_name='Teams', on_delete=models.SET_NULL, null=True)

    # Calculate average score for candidate
    def get_avg_score(self):
        average=Activity.objects.filter(candidate=self).aggregate(average_rating = Avg('activityscore_by_mentor__score'))
        return average['average_rating']

    def __str__(self):
        return self.candidate_name

    def __unicode__(self):
        return '%s' % (self.candidate_name)


class Activity(models.Model):
    song_name = models.CharField(max_length=256)
    Date_of_performance = models.DateField()
    candidate = models.ForeignKey(Candidate, related_name='Candidates', on_delete=models.CASCADE)

    # Calculate average score for activity
    def activity_avg_score(self):
        average =  list(self.activityscore_by_mentor_set.aggregate(Avg('score')).values())[0]
        return average

    def __str__(self):
        return " {} - {} - {}".format(self.song_name, self.Date_of_performance, self.candidate)


class ActivityScore_by_mentor(models.Model):
    activity = models.ForeignKey(Activity, related_name='Scores',on_delete=models.CASCADE)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    def __str__(self):
        return "ACtivity : {}, score : {}, mentor: {}".format(self.activity, self.score, self.mentor)

