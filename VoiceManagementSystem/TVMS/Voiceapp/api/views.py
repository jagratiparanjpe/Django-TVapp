from rest_framework.generics import ListAPIView, RetrieveAPIView
from ..models import Candidate, Team, Activity
from .serializers import CandidateListSerializer, CandidateDetailSerializer, TeamListSerializer, TeamDetailSerializer,ActivityListSerializer
from django.db.models import Avg, Q
from rest_framework.response import Response
### rest frameworks build in filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class ActivityListAPIView(ListAPIView):
    queryset = Activity.objects.all().annotate(average_score=Avg('Scores__score'))
    permission_classes = [IsAuthenticated]
    serializer_class = ActivityListSerializer

    # def get_queryset(self):
    #     queryset = Activity.objects.all().annotate(average_score=Avg('Scores__score'))
    #     print(queryset)
    #     return queryset


class CandidateListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Candidate.objects.all()
    serializer_class = CandidateListSerializer

class CandidateDetailsView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Candidate.objects.all()
    serializer_class = CandidateDetailSerializer

class TeamListAPIView(ListAPIView):
    serializer_class = TeamListSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get_queryset(self):
        query = self.request.GET.get('q')
        if (query):
            teams_activity_score = Team.objects.filter(Q(team_name__icontains=query)).annotate(
            average_score=Avg('Teams__Candidates__Scores__score'))
        else:
            teams_activity_score = Team.objects.all().annotate(average_score=Avg('Teams__Candidates__Scores__score'))

        return teams_activity_score


class TeamDetailsAPIView(RetrieveAPIView):
    queryset = Team.objects.all()

    permission_classes = [IsAdminUser, IsAuthenticated]
    lookup_field = 'pk'
    serializer_class = TeamDetailSerializer

