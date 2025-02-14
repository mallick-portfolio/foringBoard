from django.shortcuts import render

from project.serializers import ProjectSerializer
from .models import Project

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import logging
logger = logging.getLogger('django')

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permissions_classes = [permissions.IsAuthenticated]
    queryset = Project.objects.all()
    model = Project

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return Response(
                {
                "message": "Project created successfully!", 
                 "data": response.data
                 },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.error(
                f"Error creating project by user {request.user.email}: {str(e)}"
            )
            return Response(
                {
                    "error": "Failed to create project.", 
                    "details": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return Response(
                {
                    "message": "Project updated successfully!", 
                    "data": response.data
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(
                f"Error updating project {self.get_object().name}: {str(e)}"
            )
            return Response(
                {
                    "error": "Failed to update project.", 
                    "details": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        project_name = instance.name
        try:
            instance.delete()
            return Response(
                {
                    "message": f"Project '{project_name}' deleted successfully!"
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            logger.error(
                f"Error deleting project {project_name}: {str(e)}"
            )
            return Response(
                {
                    "error": f"Failed to delete project '{project_name}'.", 
                    "details": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )