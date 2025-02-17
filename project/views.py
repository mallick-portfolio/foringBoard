
from project.serializers import (
    ProjectSerializer, 
    TaskSerializer, 
    CommentSerializer
)
from .models import Project, Task, Comment
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

import logging
logger = logging.getLogger('django')

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Project.objects.all()
    model = Project

    def list(self, request, *args, **kwargs):
        try:
            response = self.get_queryset()
            serializer = self.get_serializer(response, many=True)
            return Response(
                {
                "message": "Project retrive successfully!", 
                 "data": serializer.data
                 },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Error in ProjectViewSet list method: {str(e)}")
            return Response(
                {
                    "error": "Failed to retrive projects.", 
                    "details": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
    
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        try:
            return Response(
                {
                    "message": "Project retrieved successfully!",
                    "data": serializer.data
                    },
                    status=status.HTTP_200_OK,
                    )
        except Exception as e:
            logger.error(
                f"Error retrieving project {instance.name}: {str(e)}"
                )
            return Response(
                {
                    "error": "Failed to retrieve project.",
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
    @action(detail=True, methods=['get', 'post'], url_path='tasks')
    def tasks(self, request, pk=None):
        """
        GET: Retrieve all tasks associated with the specified project.
        POST: Create a new task under the specified project.
        """
        try:
            project = self.get_object()
            
            if request.method == 'GET':
                try:
                    tasks = project.tasks.all()
                    serializer = TaskSerializer(tasks, many=True)
                    return Response(
                        {
                            "message": "Tasks retrieved successfully!",
                            "data": serializer.data,
                            
                        }, status=status.HTTP_200_OK)
                except Exception as e:
                    logger.error(
                        f"Error retrieving tasks for project {project.name}: {str(e)}"
                    )
                    return Response(
                        {
                            "error": "Failed to retrieve tasks.", 
                            "details": str(e)
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                
            elif request.method == 'POST':
                data = request.data.copy()
                data['project'] = project.id
                try:
                    serializer = TaskSerializer(data=data, context={'request': request})
                    if serializer.is_valid():
                        serializer.save()
                        return Response(
                        {
                            "message": "Task created successfully!", 
                            "data": serializer.data
                        },
                        status=status.HTTP_201_CREATED,
                        )
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    logger.error(
                        f"Error creating task for project {project.name}: {str(e)}"
                    )
                    return Response(
                        {
                            "error": "Failed to create task.", 
                            "details": str(e)
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND
            )


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permissions_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()
    model = Task

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(
                {
                    "message": "Task retrived successfully!", 
                    "data": serializer.data
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(
                f"Task not found: {str(e)}"
            )
            return Response(
                {
                    "error": "Task not found.", 
                    "details": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return Response(
                {
                    "message": "Task updated successfully!", 
                    "data": response.data
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(
                f"Error updating Task {self.get_object().name}: {str(e)}"
            )
            return Response(
                {
                    "error": "Failed to update Task.", 
                    "details": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        task_name = instance.title
        try:
            instance.delete()
            return Response(
                {
                    "message": f"Task '{task_name}' deleted successfully!"
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            logger.error(
                f"Error deleting task {task_name}: {str(e)}"
            )
            return Response(
                {
                    "error": f"Failed to delete task '{task_name}'.", 
                    "details": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            ) 
        

    @action(detail=True, methods=['get', 'post'], url_path='comments')
    def comments(self, request, pk=None):
        """
        GET: Retrieve all comments associated with the specified task.
        POST: Create a new comment under the specified task.
        """
        try:
            task = self.get_object()
            
            if request.method == 'GET':
                try:
                    comments = task.comments.all()
                    serializer = CommentSerializer(comments, many=True)
                    return Response(
                        {
                            "message": "Comments retrieved successfully!",
                            "data": serializer.data,
                            
                        }, status=status.HTTP_200_OK)
                except Exception as e:
                    logger.error(
                        f"Error retrieving Comments for task {task.title}: {str(e)}"
                    )
                    return Response(
                        {
                            "error": "Failed to retrieve comments.", 
                            "details": str(e)
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                
            elif request.method == 'POST':
                data = request.data.copy()
                data['task'] = task.id
                try:
                    serializer = CommentSerializer(data=data, context={'request': request})
                    if serializer.is_valid():
                        serializer.save()
                        return Response(
                        {
                            "message": "Comment created successfully!", 
                            "data": serializer.data
                        },
                        status=status.HTTP_201_CREATED,
                        )
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    logger.error(
                        f"Error creating comment for task {task.name}: {str(e)}"
                    )
                    return Response(
                        {
                            "error": "Failed to create comment.", 
                            "details": str(e)
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                
        except Project.DoesNotExist:
            return Response(
                {"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND
            )
        



class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permissions_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    model = Comment

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(
                {
                    "message": "Commment retrived successfully!", 
                    "data": serializer.data
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(
                f"Commment not found: {str(e)}"
            )
            return Response(
                {
                    "error": "Commment not found.", 
                    "details": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return Response(
                {
                    "message": "Commment updated successfully!", 
                    "data": response.data
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(
                f"Error updating Commment {self.get_object().name}: {str(e)}"
            )
            return Response(
                {
                    "error": "Failed to update Commment.", 
                    "details": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        comment_id = instance.id
        try:
            instance.delete()
            return Response(
                {
                    "message": f"Commment '{comment_id}' deleted successfully!"
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            logger.error(
                f"Error deleting project {comment_id}: {str(e)}"
            )
            return Response(
                {
                    "error": f"Failed to delete comment '{comment_id}'.", 
                    "details": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST,
            ) 
        

        """
        GET: Retrieve all comments associated with the specified task.
        POST: Create a new comment under the specified task.
        """
        try:
            task = self.get_object()
            
            if request.method == 'GET':
                try:
                    comments = task.comments.all()
                    serializer = CommentSerializer(comments, many=True)
                    return Response(
                        {
                            "message": "Comments retrieved successfully!",
                            "data": serializer.data,
                            
                        }, status=status.HTTP_200_OK)
                except Exception as e:
                    logger.error(
                        f"Error retrieving Comments for task {task.title}: {str(e)}"
                    )
                    return Response(
                        {
                            "error": "Failed to retrieve comments.", 
                            "details": str(e)
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                
            elif request.method == 'POST':
                data = request.data.copy()
                data['task'] = task.id
                try:
                    serializer = CommentSerializer(data=data, context={'request': request})
                    if serializer.is_valid():
                        serializer.save()
                        return Response(
                        {
                            "message": "Comment created successfully!", 
                            "data": serializer.data
                        },
                        status=status.HTTP_201_CREATED,
                        )
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    logger.error(
                        f"Error creating comment for task {task.name}: {str(e)}"
                    )
                    return Response(
                        {
                            "error": "Failed to create comment.", 
                            "details": str(e)
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                
        except Project.DoesNotExist:
            return Response(
                {"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND
            )