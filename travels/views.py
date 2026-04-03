from django.shortcuts import render
from rest_framework import viewsets
from .models import Project, Place
from .serializers import ProjectSerializer, PlaceSerializer
from rest_framework.response import Response
from rest_framework import status
from .services.artic import validate_place

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_update(self, serializer):
        place = serializer.save()
        place.project.update_completion()

    def create(self, request, *args, **kwargs):
        places_data = request.data.get('places', [])

        if len(places_data) > 10:
            return Response({"error": "Max 10 places"}, status=400)

        project = Project.objects.create(
            name=request.data.get('name'),
            description=request.data.get('description'),
            start_date=request.data.get('start_date')
        )

        for place in places_data:
            ext_id = place.get('external_id')

            if not validate_place(ext_id):
                return Response({"error": f"Place {ext_id} not found"}, status=400)

            Place.objects.create(project=project, external_id=ext_id)

        return Response(ProjectSerializer(project).data)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()

        if project.places.filter(visited=True).exists():
            return Response({"error": "Cannot delete project"}, status=400)

        project.delete()
        return Response(status=204)


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def perform_update(self, serializer):
        place = serializer.save()
        place.project.update_completion()

    def perform_create(self, serializer):
        project = serializer.validated_data['project']

        if project.places.count() >= 10:
            raise Exception("Max 10 places")

        ext_id = serializer.validated_data['external_id']

        if not validate_place(ext_id):
            raise Exception("Invalid place")

        serializer.save()