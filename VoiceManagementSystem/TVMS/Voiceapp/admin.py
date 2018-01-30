from django.contrib import admin
from .models import Team, Candidate, Activity, ActivityScore_by_mentor
# Register your models here.
# Define the admin class
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'mentor')


admin.site.register(Team, TeamAdmin)
admin.site.register(Candidate)
admin.site.register(Activity)
admin.site.register(ActivityScore_by_mentor)