from rest_framework import serializers
from .models import Project, Place


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'external_id', 'notes', 'visited', 'project']

    def update(self, instance, validated_data):
        instance.notes = validated_data.get('notes', instance.notes)
        instance.visited = validated_data.get('visited', instance.visited)
        instance.save()
        return instance


class ProjectSerializer(serializers.ModelSerializer):
    places = PlaceSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'is_completed', 'places']
        read_only_fields = ['is_completed']