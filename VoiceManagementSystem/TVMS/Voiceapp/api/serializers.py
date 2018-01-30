from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from ..models import Candidate, Team, Activity
from django.db.models import Avg

## Activity List Serializer
class ActivityListSerializer(ModelSerializer):
   # annoated field on activity object
   average_score = serializers.DecimalField(max_digits=5, decimal_places=2)
   class Meta:
        model = Activity
        fields = [
            'song_name',
            'Date_of_performance',
            'candidate',
            'average_score',
        ]

## Candiadte List Serializer
class CandidateListSerializer(ModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            'candidate_name',
            'team'
        ]

## Candidate Detail Serializer
class CandidateDetailSerializer(ModelSerializer):
    activity=serializers.SerializerMethodField()
    class Meta:
        model = Candidate
        fields = [
            'candidate_name',
            'team',
            'activity'
        ]
    def get_activity(self,obj):
        activity_qs = Activity.objects.filter(candidate=obj)
        activities = CandidateDetailSerializer(activity_qs, many=True).data
        return activities

## Team List Serializer
class TeamListSerializer(ModelSerializer):
    average_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    class Meta:
        model = Team
        fields = [
            'team_name',
            'mentor',
            'average_score'
        ]

## Team Detail Serializer
class TeamDetailSerializer(ModelSerializer):
    candidate_activity= serializers.SerializerMethodField()
    class Meta:
        model = Team
        fields = [
            'team_name',
            'mentor',
            'candidate_activity',
        ]
    def get_candidate_activity(self, obj):
        candidate_activities_qs = Activity.objects.select_related('candidate__team').annotate(average_score=Avg('Scores__score')).filter(candidate__team=obj)
        activities = ActivityListSerializer(candidate_activities_qs, many=True).data
        return activities
        # working code
        # candidate_qs= Candidate.objects.filter(team=obj)
        # candidates = CandidateDetailSerializer(candidate_qs, many=True).data
        # return candidates




