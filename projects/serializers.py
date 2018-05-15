from rest_framework import serializers
from .models import Project, Dataset, User

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'description', 'start_date', 'finish_date', 'pk')

